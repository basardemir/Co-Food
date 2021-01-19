from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length
from services.restaurant import *


class MenuEditForm(FlaskForm):
    price = FloatField(
        'price',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100)
        ]
    )
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=128, message="wrong"),
                       ])
    description = TextAreaField("description",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256, message="wrong"),
                                ])
    ingredients = TextAreaField("ingredients",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256, message="wrong"),
                                ])
    campaign = BooleanField("campaign")
    res_choice = getAllRestaurantsForm()
    restaurant = SelectField("restaurant", validate_choice=False, choices=res_choice
                             )

class MenuEditOwnerForm(FlaskForm):
    price = FloatField(
        'price',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100)
        ]
    )
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=128, message="wrong"),
                       ])
    description = TextAreaField("description",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256, message="wrong"),
                                ])
    ingredients = TextAreaField("ingredients",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256, message="wrong"),
                                ])
    campaign = BooleanField("campaign")
    res_choice = getAllRestaurantsForm()