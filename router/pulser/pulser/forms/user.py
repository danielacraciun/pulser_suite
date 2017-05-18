# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, AnyOf

from pulser.models.user import User


class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    first_name = TextField('First Name', validators=[DataRequired(), Length(min=3, max=25)])
    last_name = TextField('Last Name', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])


class UsernameForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    username2 = StringField('Confirm Username',
                            validators=[DataRequired(), EqualTo('username', message='Usernames must match')])

class CareReceiverForm(Form):
    first_name = TextField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    last_name = TextField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    age = IntegerField("Age", validators=[NumberRange(18, 120, "Age is out of range."), Optional()])
    weight = IntegerField("Weight", validators=[NumberRange(20, 400, "Weight is out of range."), Optional()])
    height = IntegerField("Height", validators=[NumberRange(100, 250, "Height is out of range."), Optional()])
    sex = IntegerField("Sex", validators=[NumberRange(0, 1, "Please choose valid gender. 0 is Male, 1 is Female")])

class MovementSensorForm(Form):
    secret_key = TextField('Secret Key', validators=[DataRequired(), Length(10)])

class HrSensorForm(Form):
    client_id = TextField('Client Id', validators=[DataRequired()])
    client_secret = TextField('Client Secret', validators=[DataRequired()])