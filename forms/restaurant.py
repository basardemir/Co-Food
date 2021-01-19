from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, validators
from wtforms.validators import DataRequired, Length, Optional

from services import category, university


class RestaurantEditForm(FlaskForm):
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=64, message="The length of the name must be shorter than 65 characters."),
                       ])
    cat_choice = category.getAllCategoriesForm()
    category = SelectField("category", validate_choice=False, choices=cat_choice)

    uni_choice = university.getAllUniversitiesAdminForm()
    university = SelectField("university", validate_choice=False, choices=uni_choice)

    menupdf = FileField("menupdf", validators=[
        Optional(),
    ])

    phone = StringField("phone", validators=[
        Length(min=1, max=11, message="The length of the name must be shorter than 11 characters.")
    ])
