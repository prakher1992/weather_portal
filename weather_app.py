from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '327027639660844979580338508137590406252'
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///data.db"
db = SQLAlchemy(app)

from models import User, City

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_1 = User(name='Prakher', email="prakher1992@gmail.com", password="password")
        db.session.add(user_1)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@weather.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/add-city", methods=['GET', 'POST'])
def add_city():
    return "Add city"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
