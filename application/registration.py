from flask import Flask, render_template, request
from passlib.hash import pbkdf2_sha256 as hasher
from services.university import getAllUniversities
from services.registration import *
from forms.registration import *
from flask import current_app, flash, redirect, url_for, session
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
    if 'role' in session:
        if session['role'] == 'student':
            student = getStudentById(user_id)
            if student:
                return User(user_id, student['username'], "student")
        if session['role'] == 'owner':
            owner = getRestaurantById(user_id)
            if owner:
                return User(user_id, owner['name'], "owner")


def register():
    form = RegisterForm()
    universities = getAllUniversities();
    return render_template("consumerViews/register.html", universities=universities, form=form)


def login():
    form = LoginForm()
    return render_template("consumerViews/login.html", form=form)


def loginClient():
    form = LoginForm()
    if form.validate_on_submit():
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']
        if request.form['role'] == "0":
            return loginStudent(username, password)
        elif request.form['role'] == "1":
            return loginRestaurant(username, password)
        else:
            return login()
        #if request.form['role'] == "2":
        #   loginAdmin(username, password)



def loginStudent(username, password):
    student = getStudent(username, password)
    if student:
        user = User(student['id'], student['username'], "student")
        login_user(user)
        session['role'] = 'student'
        flash("You have logged in.")
        next_page = request.args.get("next", url_for("homepage"))
        return redirect(next_page)
    else:
        flash("Invalid credentials.")


def loginRestaurant(name, password):
    form = LoginForm()
    if form.validate_on_submit():
        restaurant = getRestaurant(name, password)
        if restaurant:
            user = User(restaurant['id'], restaurant['name'], "owner")
            login_user(user)
            session['role'] = 'owner'
            flash("You have logged in.")
            next_page = request.args.get("next", url_for("homepage"))
            return redirect(next_page)
        else:
            flash("Invalid credentials.")
            return login()


def addClient():
    form = RegisterForm()
    if form.validate_on_submit():
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if request.form['role'] == "0":
            university = request.form['university']
            return addNewStudent(username, password, email, university)
        elif request.form['role'] == "1":
            return addNewRestaurant(username, password, email)
        else:
            return render_template("consumerViews/register.html", form=form)

def addNewStudent(username, password, email, university):
    form = RegisterForm()
    formLogin = LoginForm()
    error = []
    user = []
    user.append(username)
    user.append(hasher.hash(password))
    user.append(email)
    user.append(university)
    try:
        addStudent(user)
    except:
        return render_template("consumerViews/register.html", form=form)
    return redirect(url_for("login"))

def addNewRestaurant(name, password, email):
    form = RegisterForm()
    formLogin = LoginForm()
    error = []
    restaurant = []
    restaurant.append(name)
    restaurant.append(hasher.hash(password))
    restaurant.append(email)
    try:
        addRestaurant(restaurant)
    except:
        return render_template("consumerViews/register.html", form=form)
    return redirect(url_for("login"))

def logout_page():
    logout_user()
    if 'role' in session:
        session.pop('role')
    flash("You have logged out.")
    return redirect(url_for("login"))
