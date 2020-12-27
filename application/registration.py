from flask import Flask, render_template, request
from passlib.hash import pbkdf2_sha256 as hasher
from services.university import getAllUniversities
from services.registration import *
from forms.registration import *
from flask import current_app, flash, redirect, url_for
from flask_login import UserMixin, login_user, logout_user

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.active = True
        self.role = role
    def get_id(self):
        return self.id
    def get_role(self):
        return self.role
    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    student = getStudentById(user_id)
    if student:
        return User(user_id, student['username'], "student")
    else:
        return None

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
        student = getStudent(form.username.data, form.password.data)
        if student:
            user = User(student['id'],student['username'], "student")
            login_user(user)
            flash("You have logged in.")
            next_page = request.args.get("next", url_for("homepage"))
            return redirect(next_page)
        else:
            flash("Invalid credentials.")
    return render_template("consumerViews/login.html", form=form)

def add_user():
    form = RegisterForm()
    formLogin = LoginForm()
    error =[]
    if form.validate_on_submit():
        user =[]
        user.append(form.username.data)
        user.append(hasher.hash(form.password.data))
        user.append(form.email.data)
        user.append(form.university.data)
        try:
            addStudent(user)
        except:
            return render_template("consumerViews/register.html", form=form)
    else:
        return render_template("consumerViews/register.html", form=form)
    return redirect(url_for("login"))


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("login"))