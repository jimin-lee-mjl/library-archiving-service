import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


def passwordChecker(form, field):
    password = field.data
    min_length = 10
    alphabet = re.compile(
      '[a-zA-Z]+'
      )
    special = re.compile('\W+')
    match_alphabet = alphabet.search(password)
    match_special = special.search(password)
    if len(password) >= min_length:
        if match_alphabet and match_special:
            pass
    else:
        raise ValidationError('비밀번호는 말파벳 소문자와 대문자, 특수문자 중 두 가지를 포함해 10글자 이상이어야 합니다.')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(),
        Length(min=3, max=15, message='3글자 이상 15글자 이하로 작성해주세요.')
    ])
    email = String('Email', validators=[
        InputRequired(),
        Length(min=6, max=35, message='6글자 이상 35글자 이하로 작성해주세요.')
    ])
    password = PasswordField('Password', [
        InputRequired(),
        EqualTo('repeat_pw', message='비밀번호가 일치하지 않습니다.')
    ])
    repeat_pw = PasswordField('Confirm Password')