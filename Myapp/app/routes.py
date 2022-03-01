from app import app
from flask import render_template, url_for, redirect, flash, get_flashed_messages, request
from app.models import User
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from app.forms import RegistraionForm, LoginForm
from app import db
import requests


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect('product')
            else:
                flash("wrong username or password", category='danger')
        return render_template("login.html", form=form)
    except:
        flash("Wrong username or password", category="danger")
        return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegistraionForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data, password=form.pass1.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            if form.errors != {}:
                for error in form.errors.values():
                    flash(error)
        return render_template("register.html", form=form)
    except:
        flash("Username or email already used   ", category="danger")
        return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    try:
        if current_user.is_authenticated:
            if request.method == 'POST':
                city = request.form.get('city')
                API_KEY = '21e952d5e714564045d89667bd31bfdb'
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
                r = requests.get(url.format(city)).json()

                wth = {
                    'city': city,
                    'temperature': r['main']['temp'],
                    'description': r['weather'][0]['description'],
                    'pressure': r['main']['pressure'],
                    'humidity': r['main']['humidity'],
                    'icon': r['weather'][0]['icon'],
                    'wind': r['wind']['speed']
                }
                return render_template('weather.html', wth=wth)

            wth = {
                'city': ""
            }

            return render_template('weather.html',wth=wth)
        else:
            return redirect("login")
    except:
        flash("City doesn't exists")
        wth = {
            'city': ""
        }

        return render_template('weather.html', wth=wth)


@app.route('/product')
def product():
    return render_template('product.html')
