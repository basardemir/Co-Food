from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class orderForm(FlaskForm):
    address = TextAreaField("Address",
                            validators=[
                                DataRequired(),
                                Length(min=1, max=256, message="wrong"),
                            ])

    friendnumber = SelectField("Number of Friends", validate_choice=False, choices=[
        ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    ordercount = SelectField("Menu Count", validate_choice=False, choices=[
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
