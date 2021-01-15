from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length

from services import university


class RegisterForm(FlaskForm):
    choices = [('0', 'Student'), ('1', 'Owner')]
    role = SelectField("Role", choices=choices, validate_choice=False
                       )
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    email = EmailField("email", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    uni_choice = university.getAllUniversitiesForm();
    university = SelectField("university", validate_choice=False, choices=uni_choice
                             )
    agree = BooleanField("agree", validators=[
        DataRequired()
    ])


class LoginForm(FlaskForm):
    choices = [('0', 'Student'), ('1', 'Owner'), ('2', 'Admin')]
    username = StringField("Username",
                           validators=[
                               DataRequired(),
                               Length(min=1, max=128, message="wrong"),
                           ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    role = SelectField("Role", choices=choices, validate_choice=False
                       )
