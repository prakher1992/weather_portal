from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '327027639660844979580338508137590406252'
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///data.db"
db = SQLAlchemy(app)
# with app.app_context():
#     db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    joining_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cities = db.relationship('City', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"City('{self.city}', '{self.date_posted}')"

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
