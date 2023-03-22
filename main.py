from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data import user
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, IntegerField, DateTimeField, \
    SelectMultipleField
from wtforms.validators import DataRequired
from data.job import Jobs
import datetime
from data import job_api
from flask import make_response, jsonify
from data.users_resource import UsersResource, UsersListResource
from data.jobs_resource import JobsResource, JobsListResource
from flask_restful import abort, Api

User = user.User



class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = EmailField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    nickname = StringField("Surname", validators=[DataRequired()])
    age = IntegerField("Age")
    pos = StringField("Position")
    adrs = StringField("Address")
    submit = SubmitField("Register")


class JobForm(FlaskForm):
    # email = SelectField("Team leader email", choices=[], validators=[DataRequired()])
    name = StringField("Title of job", validators=[DataRequired()])
    w_size = IntegerField("Work size (in hours)", validators=[DataRequired()])
    collab = SelectMultipleField("Collaborators\" IDs", choices=[])
    start_date = DateTimeField("Start date", format="%Y-%m-%d %H:%M:%S",
                               default=datetime.datetime(year=2023, month=2, day=25, hour=12, minute=0, second=0))
    end_date = DateTimeField("End date", format="%Y-%m-%d %H:%M:%S",
                             default=datetime.datetime(year=2024, month=2, day=25, hour=12, minute=0, second=0))
    hazard_level = IntegerField("Hazard level", default=None)
    done = BooleanField("Is finished?")
    submit = SubmitField("Submit")


app = Flask(__name__)
api = Api(app)
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
    if current_user.is_authenticated:
        return redirect("/jobs")
    else:
        return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Register form",
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
        return redirect("/")
    return render_template("reg.html", title="Регистрация", form=form)


@app.route("/jobs")
def list_jobs():
    db_sess = db_session.create_session()
    res = db_sess.query(Jobs).all()
    data = []
    for job in res:
        title = job.job
        time = f"{round((job.end_date - job.start_date).total_seconds() / 3600)} час"
        team_leader = job.user.nickname
        collab = job.collaborators
        f = job.is_finished
        data.append([title, team_leader, time, collab, f, job.user.id, job.id])
    return render_template("jobs.html", jobs=data)


@app.route("/addjob", methods=["GET", "POST"])
@login_required
def addjob():
    form = JobForm()
    _tmp = db_session.create_session()
    _res = _tmp.query(User).all()
    for _i in _res:
        form.collab.choices.append(str(_i.id))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.name.data
        job.team_leader = current_user.id
        job.collaborators = ",".join(form.collab.data)
        job.is_finished = form.done.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.work_size = form.w_size.data
        db_sess.add(job)
        db_sess.commit()
        return redirect("/jobs")
    return render_template("job_add.html", title="Добавление работы", form=form)


if __name__ == "__main__":
    db_session.global_init("db/users.db")
    app.register_blueprint(job_api.blueprint)
    api.add_resource(UsersListResource, '/api2/users')
    api.add_resource(UsersResource, '/api2/users/<int:user_id>')
    api.add_resource(JobsListResource, '/api2/jobs')
    # для одного объекта
    api.add_resource(JobsResource, '/api2/jobs/<int:job_id>')
    app.run()
    app.run(port=8080, host="127.0.0.1")
