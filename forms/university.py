from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class UniversityEditForm(FlaskForm):
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=128, message="The length of the name must be shorter than 129 characters.")
                       ])
