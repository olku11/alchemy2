from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data import user
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired
from data.job import Jobs

User = user.User


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    nickname = StringField("Surname", validators=[DataRequired()])
    age = IntegerField("Age")
    pos = StringField("Position")
    adrs = StringField("Address")
    submit = SubmitField("Register")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def base():
    if current_user.is_authenticated:
        return redirect("/jobs")
    else:
        return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user1 = User(
            nickname=form.nickname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.pos.data,
            address=form.adrs.data
        )
        user1.set_password(form.password.data)
        db_sess.add(user1)
        db_sess.commit()
        return redirect('/')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/jobs')
def list_jobs():
    db_sess = db_session.create_session()
    res = db_sess.query(Jobs).all()
    data = []
    for job in res:
        title = job.job
        time = f'{round((job.end_date - job.start_date).total_seconds() / 3600)} hours'
        team_leader = job.user.nickname
        collab = job.collaborators
        f = job.is_finished
        data.append([title, team_leader, time, collab, f, job.user.id, job.id])
    return render_template('jobs.html', jobs=data)


if __name__ == '__main__':
    db_session.global_init('db/users.db')
    app.run(port=8080, host='127.0.0.1')
