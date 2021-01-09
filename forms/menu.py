from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, FloatField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

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
    campaign = BooleanField("campaign")
