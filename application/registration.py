from flask import current_app, flash, redirect, url_for, session
from flask import render_template, request
from flask_login import UserMixin, login_user, logout_user

from forms.registration import *
from services.registration import *
from services.university import getAllUniversities


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
        if session['role'] == 'admin':
            return User("admin", "admin", "admin")


def register():
    form = RegisterForm()
    universities = getAllUniversities()
    return render_template("consumerViews/register.html", universities=universities, form=form)


def login():
    form = LoginForm()
    success = request.args.get('success')
    if success == 'true':
        return render_template("consumerViews/login.html", form=form,success='true')
    return render_template("consumerViews/login.html", form=form)


def loginClient():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']
        if request.form['role'] == "0":
            return loginStudent(username, password)
        elif request.form['role'] == "1":
            return loginRestaurant(username, password)
        else:
            return loginAdmin(username, password)
    else:
        return render_template("consumerViews/login.html", form=form)


def loginStudent(username, password):
    form = LoginForm()
    student = getStudent(username, password)
    if student:
        user = User(student['id'], student['username'], "student")
        login_user(user)
        session['role'] = 'student'
        session['id'] = student['id']
        next_page = request.args.get("next", url_for("homepage"))
        return redirect(next_page)
    else:
        return render_template("consumerViews/login.html", form=form, messages=["Invalid credentials."])


def loginRestaurant(name, password):
    form = LoginForm()
    restaurant = getRestaurant(name, password)
    if restaurant:
        user = User(restaurant['id'], restaurant['name'], "owner")
        login_user(user)
        session['role'] = 'owner'
        session['id'] = restaurant['id']
        flash("You have logged in.")
        next_page = request.args.get("next", url_for("ownerhomepage"))
        return redirect(next_page)
    else:
        return render_template("consumerViews/login.html", form=form, messages=["Invalid credentials."])


def loginAdmin(name, password):
    form = LoginForm()
    admin_password = current_app.config["PASSWORDS"].get("admin")
    if hasher.verify(password, admin_password) and name == "admin":
        user = User("admin", "admin", "admin")
        login_user(user)
        session['role'] = 'admin'
        flash("You have logged in.")
        next_page = request.args.get("next", url_for("adminhomepage"))
        return redirect(next_page)
    else:
        return render_template("consumerViews/login.html", form=form, messages=["Invalid credentials."])


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
            phone = request.form['phone']
            return addNewRestaurant(username, password, email, phone)
        else:
            return render_template("consumerViews/register.html", form=form)
    else:
        return render_template("consumerViews/register.html", form=form)


def addNewStudent(username, password, email, university):
    form = RegisterForm()
    user = []
    user.append(username)
    user.append(hasher.hash(password))
    user.append(email)
    user.append(university)
    try:
        add = addStudent(user)
        if add != True:
            return render_template("consumerViews/register.html", form=form, messages=["Error: " + add])
    except:
        return render_template("consumerViews/register.html", form=form, messages=["Check your information."])

    return redirect(url_for("login", success='true'))


def addNewRestaurant(name, password, email, phone):
    form = RegisterForm()
    restaurant = []
    restaurant.append(name)
    restaurant.append(hasher.hash(password))
    restaurant.append(email)
    restaurant.append(phone)
    try:
        add = addRestaurant(restaurant)
        if add != True:
            return render_template("consumerViews/register.html", form=form, messages=["Error: " + add])
    except:
        return render_template("consumerViews/register.html", form=form, messages=["Check your information."])
    return redirect(url_for("login", success='true'))


def logout_page():
    logout_user()
    if 'role' in session:
        session.pop('role')
    flash("You have logged out.")
    return redirect(url_for("login"))
