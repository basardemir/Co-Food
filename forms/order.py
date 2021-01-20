from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from services.menu import getAllMenusForm
from services.students import getAllStudentsForm, getAllStudentsAddForm


class orderForm(FlaskForm):
    address = TextAreaField("Address",
                            validators=[
                                DataRequired(),
                                Length(min=1, max=256,
                                       message="The length of the address must be shorter than 257 characters.")
                            ])
    friendnumber = SelectField("Number of Friends", validate_choice=False, choices=[
        ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    ordercount = SelectField("Menu Count", validate_choice=False, choices=[
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])


class orderEditForm(FlaskForm):
    address = TextAreaField("Address",
                            validators=[
                                DataRequired(),
                                Length(min=1, max=256,
                                       message="The length of the address must be shorter than 257 characters.")
                            ])
    friendnumber = SelectField("Number of Friends", validate_choice=False, choices=[
        ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    ordercount = SelectField("Menu Count", validate_choice=False, choices=[
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    menu_choice = getAllMenusForm()
    menu = SelectField("menu", validate_choice=False, choices=menu_choice)
    students = getAllStudentsForm()

    student = SelectField("student", validate_choice=False, choices=students)


class orderAddForm(FlaskForm):
    address = TextAreaField("Address",
                            validators=[
                                DataRequired(),
                                Length(min=1, max=256,
                                       message="The length of the address must be shorter than 257 characters.")
                            ])
    friendnumber = SelectField("Number of Friends", validate_choice=False, choices=[
        ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    ordercount = SelectField("Menu Count", validate_choice=False, choices=[
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    menu_choice = getAllMenusForm()
    menu = SelectField("menu", validate_choice=False, choices=menu_choice)
    students = getAllStudentsAddForm()
    student = SelectField("student", validate_choice=False, choices=students)
