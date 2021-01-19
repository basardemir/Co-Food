from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional

from services import university


class SettingsForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    email = EmailField("email", validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong")
    ])
    password = PasswordField("password", validators=[
        Length(min=1, max=128, message="wrong"),
         Optional()
    ])
    uni_choice = university.getAllUniversitiesForm()
    university = SelectField("university", validate_choice=False, choices=uni_choice)
    passwordchange = BooleanField("passwordchange",validators=[
        Optional()
    ])