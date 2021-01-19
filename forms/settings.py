from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional

from services import university


class SettingsForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=1, max=64, message="The length of the name must be shorter than 65 characters.")
    ])
    email = EmailField("email", validators=[
        DataRequired(),
        Length(min=1, max=64, message="The length of the email must be shorter than 65 characters.")
    ])
    password = PasswordField("password", validators=[
        Length(min=1, max=256, message="The length of the comment must be shorter than 257 characters."),
        Optional()
    ])
    uni_choice = university.getAllUniversitiesForm()
    university = SelectField("university", validate_choice=False, choices=uni_choice)
    passwordchange = BooleanField("passwordchange", validators=[
        Optional()
    ])
