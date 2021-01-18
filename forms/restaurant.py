from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,FileField,validators
from wtforms.validators import DataRequired, Length

from services import category, university


class RestaurantEditForm(FlaskForm):
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=128, message="wrong"),
                       ])
    cat_choice = category.getAllCategoriesForm()
    category = SelectField("category", validate_choice=False, choices=cat_choice
                           )
    uni_choice = university.getAllUniversitiesAdminForm()
    university = SelectField("university", validate_choice=False, choices=uni_choice
                             )
    menupdf = FileField("menupdf")
