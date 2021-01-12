from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, FloatField, TextAreaField, DecimalField, \
    RadioField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class CommentAddForm(FlaskForm):
    comment = TextAreaField("comment",
                                validators=[
                                    DataRequired(),
                                    Length(min=1, max=256, message="wrong"),
                                ])
    rate = RadioField("rate", choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])