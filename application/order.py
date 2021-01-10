from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.university import *
from services.comment import *
from services.service import *
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from forms.restaurant import RestaurantEditForm
from forms.order import *
from flask import redirect, url_for
from flask import Flask, render_template, request
from flask import current_app
from flask_login import UserMixin
from services.university import getAllUniversities
from flask import current_app, flash, redirect, url_for, session

def orderPage(menuId):
    if session['role'] == 'student':
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant:
            form = orderForm()
            return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                               form=form)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


def insertOrder(menuId):
    form = orderForm()
    if session['role'] == 'student':
        if form.validate_on_submit():
            if(searchActiveOrders(session['id']))


        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant:
            form = orderForm()
            return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                               form=form)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")