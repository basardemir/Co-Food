from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional

from services import university


class RegisterForm(FlaskForm):
    choices = [('0', 'Student'), ('1', 'Owner')]
    role = SelectField("Role", choices=choices, validate_choice=False
                       )
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=64, message="The length of the name must be shorter than 65 characters.")
    ])
    email = EmailField("email", validators=[
        DataRequired(),
        Length(min=1, max=64, message="The length of the email must be shorter than 65 characters.")
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=1, max=256, message="The length of the password must be shorter than 257 characters.")
    ])
    phone = StringField("phone", validators=[
        Optional(),
        Length(min=1, max=16, message="The length of the phone number must be shorter than 17 characters.")
    ])
    uni_choice = university.getAllUniversitiesForm()
    university = SelectField("university", validate_choice=False, choices=uni_choice
                             )
    agree = BooleanField("agree", validators=[
        DataRequired()
    ])


class LoginForm(FlaskForm):
    choices = [('0', 'Student'), ('1', 'Owner'), ('2', 'Admin')]
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=1, max=64, message="The length of the name must be shorter than 65 characters.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=1, max=256, message="The length of the password must be shorter than 257 characters.")
    ])
    role = SelectField("Role", choices=choices, validate_choice=False)
