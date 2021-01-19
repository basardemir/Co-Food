from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import DataRequired, Length


class CommentAddForm(FlaskForm):
    comment = TextAreaField("comment",
                            validators=[
                                DataRequired(),
                                Length(min=1, max=256, message="The length of the comment must be shorter than 257 characters."),
                            ])
    rate = RadioField("rate", choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
