from flask import Flask, render_template, request
from services.university import getAllUniversities
from services.registration import *
from forms.registration import *

def register():
    form = RegisterForm()
    universities = getAllUniversities();
    return render_template("consumerViews/register.html", universities = universities, form=form)

def login():
    form = LoginForm()
    return render_template("consumerViews/login.html",form=form)


def loginStudent():
    form = LoginForm()
    if form.validate_on_submit():
        check = checkStudent(form.username.data, form.password.data)
        if check:
            print("dogru")
        else:
            print("yanlış")
    else:
        print("else")
    return render_template("consumerViews/login.html", form=form)

def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        user =[]
        user.append(form.username.data)
        user.append(form.password.data)
        user.append(form.email.data)
        user.append(form.university.data)
        addStudent(user)
        print("kndskanfdlknasdlkfnsdlkfn")
    else:
        print("else")
    return render_template("consumerViews/login.html")