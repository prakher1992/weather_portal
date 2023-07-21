from datetime import datetime
from weather_app import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    joining_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cities = db.relationship('City', backref='author', lazy=True)
    notify = db.relationship('Notification', backref='creater', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_temp_notified = db.Column(db.Boolean, nullable = False, default= False)
    is_weather_notified = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"City('{self.city}', '{self.date_posted}')"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notify_condition = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Notification('{self.type}', '{self.notify_condition}')"