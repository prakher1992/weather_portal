from flask import render_template, url_for, flash, redirect, request
from weather_app import app, db, bcrypt
from weather_app.forms import RegistrationForm, LoginForm, CityForm
from weather_app.models import User,City
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home():
    cities = City.query.all()
    return render_template('home.html', cities=cities)

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
    return redirect(url_for('home'))

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