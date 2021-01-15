from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryEditForm(FlaskForm):
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=128, message="wrong"),
                       ])
