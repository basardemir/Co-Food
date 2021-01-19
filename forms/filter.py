from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length, Optional

from services import category


class RestaurantSearchForm(FlaskForm):
    restaurantname = StringField("restaurantname", validators=[
        Length(min=0, max=64, message="The length of the name must be shorter than 65 characters."),
        Optional()
    ])
    category_choice = category.getAllCategoriesForm()
    categories = SelectField("categories", validate_choice=False, choices=category_choice)


class CampaignSearchForm(FlaskForm):
    menuname = StringField("menuname", validators=[
        Length(min=0, max=64, message="The length of the name must be shorter than 65 characters."),
        Optional()
    ])
    category_choice = category.getAllCategoriesForm()
    categories = SelectField("categories", validate_choice=False, choices=category_choice)
