from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms_components import IntegerField
from services import category,university


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
