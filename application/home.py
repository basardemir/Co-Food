from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from services.order import *


@login_required
def homepage():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        orders = getAllOrders()
        return render_template("consumerViews/main_page.html", form=form, orders=orders)
    else:
        return render_template("errorViews/403.html")


@login_required
def ownerhomepage():
    if session['role'] == 'owner':
        return render_template("ownerViews/owner_home.html")
    else:
        return render_template("errorViews/403.html")

@login_required
def adminhomepage():
    if session['role'] == 'admin':
        return render_template("adminViews/admin_home.html")
    else:
        return render_template("errorViews/403.html")

@login_required
def filter_homepage():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        return render_template("consumerViews/main_page.html", form=form)
    else:
        return render_template("errorViews/403.html")