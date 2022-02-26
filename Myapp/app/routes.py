from app import app
from flask import render_template, url_for, redirect, flash, get_flashed_messages
from app.models import User
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from app.forms import RegistraionForm, LoginForm
from app import db


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect('/')
        else:
            flash("wrong username or password", category='danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistraionForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.pass1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(error)
    return render_template("register.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
