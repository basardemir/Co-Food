from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.order import *
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

def activeOrder():
    if session['role'] == 'student':
        studentId = session['id']
        order=getOrderDetails(studentId)
        friends = getOrderFriends(order['id'])
        friendsize = len(friends)
        if order and friends:
            return render_template("consumerViews/wait_room.html", order=order, friends=friends,friendsize=friendsize)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")

def insertNewOrder(menuId):
    form = orderForm()
    if session['role'] == 'student':
        if form.validate_on_submit():
            if (hasActiveOrder(session['id'])):
                menu = getMenuById(menuId)
                restaurant = getRestaurantById(menu['restaurantid'])
                if menu and restaurant:
                    form = orderForm()
                    return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                                           form=form, message="You have non-delivered order.")
                else:
                    return render_template("errorViews/404.html")
            else:
                if (insertOrderSQL(menuId, session['id'], form['friendnumber'].data, 3, "bsbfbsfbs")):
                    return redirect("/activeorder")
                else:
                    form = orderForm()
                    menu = getMenuById(menuId)
                    restaurant = getRestaurantById(menu['restaurantid'])
                    return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                               form=form, message="An error occurred, try again!")

    else:
        return render_template("errorViews/403.html")
