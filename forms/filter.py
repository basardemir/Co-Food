from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms_components import IntegerField
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