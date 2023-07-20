from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from weather_app.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CityForm(FlaskForm):
    city = StringField("City",validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add')

class TemperatureNotifyForm(FlaskForm):
    notify_condition = IntegerField("Temperature",validators=[DataRequired(), Length(max=3)])
    submit = SubmitField('Add')

class WeatherNotifyForm(FlaskForm):
    notify_condition = StringField("Weather",validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Add')

