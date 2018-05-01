from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required, Regexp
from simpledu.models import db, User
from wtforms import ValidationError
import re

class RegisterForm(FlaskForm):
    #username = StringField('Username', validators=[Required(), Length(3, 24), Regexp('^[A-Za-z0-9]*$',0,'name is invalid')])
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username used')
        else:
            if not re.match('^[A-Za-z0-9]*$',field.data):
                flash('用户名只支持字母和数字','danger')
                raise ValidationError('用户名错误')
            else:
                pass
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email used')
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    #email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    #def validate_email(self, field):
    #    if field.data and not User.query.filter_by(email=field.data).first():
    #        raise ValidationError('email not register')
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('username not register')
    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Password error')
    submit = SubmitField('Submit')
