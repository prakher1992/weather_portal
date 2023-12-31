from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from weather_app import app, db, bcrypt
from weather_app.forms import RegistrationForm, LoginForm, CityForm, TemperatureNotifyForm, WeatherNotifyForm
from weather_app.models import User,City, Notification
from flask_login import login_user, current_user, logout_user, login_required
import requests

@app.route('/')
@app.route('/home')
@login_required
def home():
    cities = current_user.cities
    city_list= list()
    for city in cities:
        d = weather(city.city)
        if d:
            d["id"] = city.id
            city_list.append(d)
    return render_template('home.html', cities=city_list)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/add-city", methods=['GET', 'POST'])
@login_required
def add_city():
    form = CityForm()
    if form.validate_on_submit():
        city = City(city=form.city.data, author=current_user)
        db.session.add(city)
        db.session.commit()
        flash('New City added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_city.html', title='New City', form=form)


@app.route("/city/<int:city_id>/delete", methods=['GET'])
@login_required
def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    if city.author != current_user:
        abort(403)
    db.session.delete(city)
    db.session.commit()
    flash('Your city has been deleted!', 'success')
    return redirect(url_for('home'))


def weather(city):
    apikey = "Your_Key"
    source = requests.get('https://api.openweathermap.org/data/2.5/weather',
                          params={'q':city,"appid":apikey}, verify=False).json()
    if source.get("cod") == 200:
        country = source["sys"]["country"]
        temp = source["main"]["temp"]-273.15
        weather_desc = source["weather"][0]["description"]
        humidity  = source["main"]["humidity"]
        wind_speed = source["wind"]["speed"]
        weather_data = {"city":f"{city}, {country}",
                        "temp" :"{:2f} deg C".format(temp),
                        "weather_desc": weather_desc,
                        "humidity" : f"{humidity}%",
                        "wind_speed": f"{wind_speed} kmph"}
        return weather_data
    return None

@app.route('/current_loc/<string:city>', methods=['GET'])
@login_required
def current_loc(city):
    if not current_user.cities:
        city_data = City(city=city, author=current_user)
        db.session.add(city_data)
        db.session.commit()
    return jsonify({'city': city,"message":"success"})


@app.route('/set-alert', methods=['GET','POST'])
@login_required
def select_type():
    return render_template('type-alert.html', title='Select Alert Type')

@app.route('/notify/<string:notification_type>', methods=['GET','POST'])
@login_required
def add_notification(notification_type):
    types = ["temperature","weather"]
    if notification_type not in types:
        abort(404)
    if notification_type ==types[0]:
        form = TemperatureNotifyForm()
    elif notification_type ==types[1]:
        form = WeatherNotifyForm()
    if form.validate_on_submit():
        notification = Notification(notify_condition=form.notify_condition.data, creater=current_user,type=notification_type)
        db.session.add(notification)
        db.session.commit()
        flash('New Notification Condition added successfully!', 'success')
        return redirect(url_for('select_type'))
    return render_template('set-alert.html', form=form)
