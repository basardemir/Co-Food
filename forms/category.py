from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryEditForm(FlaskForm):
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=64,
                                  message="The length of the name must be shorter than 65 characters."),
                       ])
