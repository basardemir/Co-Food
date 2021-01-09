from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms_components import IntegerField
from services import university


class UniversityEditForm(FlaskForm):
    name = StringField("name",
    validators=[
        DataRequired(),
        Length(min=1, max=128, message="wrong"),
    ])
