from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms_components import IntegerField

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    email = StringField("email", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    university = SelectField("university", validate_choice=False
    )
    agree = BooleanField("agree", validators=[
        DataRequired()
    ])


class LoginForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])