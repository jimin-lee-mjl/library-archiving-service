import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError
from error_msg import AUTH_ERROR


def password_checker(form, field):
    password = field.data
    min_length = 10
    alphabet = re.compile(
      '[a-zA-Z0-9]+'
      )
    special = re.compile('\W+')
    is_alphabet = alphabet.search(password)
    is_special = special.search(password)
    if len(password) >= min_length:
        if is_alphabet and is_special:
            pass
    else:
        raise ValidationError(AUTH_ERROR['pw_not_vaild'])


def email_checker(form, field):
    email = field.data
    try:
        valid = validate_email(email)
        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        raise ValidationError(AUTH_ERROR['email_not_vaild'])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(),
        Length(min=3, max=15, message=AUTH_ERROR['username_not_valid'])
    ])
    email = StringField('Email', validators=[
        InputRequired(),
        email_checker
    ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        password_checker
    ])
    repeat_pw = PasswordField('Confirm Password', validators=[
        EqualTo('password', message=AUTH_ERROR['pw_not_match'])
    ])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired()
    ])
    password = PasswordField('Password', [
        InputRequired()
    ])