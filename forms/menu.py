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
                           Length(min=1, max=64, message="The length of the name must be shorter than 65 characters.")
                       ])
    description = TextAreaField("description",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256,
                                           message="The length of the description must be shorter than 257 characters.")
                                ])
    ingredients = TextAreaField("ingredients",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256,
                                           message="The length of the ingredients must be shorter than 257 characters.")
                                ])
    campaign = BooleanField("campaign")
    res_choice = getAllRestaurantsForm()
    restaurant = SelectField("restaurant", validate_choice=False, choices=res_choice)


class MenuEditOwnerForm(FlaskForm):
    price = FloatField(
        'price',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100, message="The possible highest price is 100TL")
        ]
    )
    name = StringField("name",
                       validators=[
                           DataRequired(),
                           Length(min=1, max=64, message="The length of the name must be shorter than 65 characters.")
                       ])
    description = TextAreaField("description",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256,
                                           message="The length of the description must be shorter than 257 characters.")
                                ])
    ingredients = TextAreaField("ingredients",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256,
                                           message="The length of the ingredients must be shorter than 257 characters.")
                                ])
    campaign = BooleanField("campaign")
