from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length

from services import category


class RestaurantSearchForm(FlaskForm):
    restaurantname = StringField("restaurantname", validators=[
        Length(min=1, max=128, message="wrong")
    ])
    category_choice = category.getAllCategoriesForm()
    categories = SelectField("categories", validate_choice=False, choices=category_choice
                             )


class CampaignSearchForm(FlaskForm):
    menuname = StringField("menuname", validators=[
        Length(min=1, max=128, message="wrong")
    ])
    category_choice = category.getAllCategoriesForm()
    categories = SelectField("categories", validate_choice=False, choices=category_choice
                             )
