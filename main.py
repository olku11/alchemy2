from flask_login import LoginManager, login_user, logout_user, login_required
from data import db_session
from data import user
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired

User = user.User


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = StringField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    nickname = StringField("Surname", validators=[DataRequired()])
    age = IntegerField("Age")
    pos = StringField("Position")
    adrs = StringField("Address")
    submit = SubmitField("Register")


app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@app.route("/index")
def base():
    """if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)"""
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("reg.html", title="Register form",
                                   form=form,
                                   message="Такой пользователь уже есть")
        user1 = User(
            email=form.email.data,
            nickname=form.nickname.data,
            age=form.age.data,
            position=form.pos.data,
            address=form.adrs.data,
        )
        user1.set_password(form.password.data)
        db_sess.add(user1)
        db_sess.commit()
        return redirect("/")
    return render_template("reg.html", title="Register form", form=form)


if __name__ == "__main__":
    db_session.global_init("db/users.db")
    app.run(port=8080, host="127.0.0.1")
