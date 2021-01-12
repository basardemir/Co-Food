from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.order import *
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
        order = getOrderDetails(studentId)
        if order:
            friends = getOrderFriends(order['id'])
            if friends:
                friendsize = len(friends)
                return render_template("consumerViews/wait_room.html", order=order, friends=friends,
                                       friendsize=friendsize)
        return redirect(url_for('homepage', noactiveorder='true', **request.args))
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

                if (
                insertOrderSQL(menuId, session['id'], int(request.form['friendnumber']) + 1, request.form['ordercount'],
                               request.form['address'])):
                    return redirect("/activeorder")
                else:
                    form = orderForm()
                    menu = getMenuById(menuId)
                    restaurant = getRestaurantById(menu['restaurantid'])
                    return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                                           form=form, message="An error occurred, try again!")

    else:
        return render_template("errorViews/403.html")


def participate(orderId):
    if session['role'] == 'student':
        studentId = session['id']
        order = getActiveOrder(orderId)
        if order and order[0]['numberofstudents'] > len(order) and not (
        hasActiveOrder(session['id'])) and insertParticipant(studentId, orderId):
            return redirect("/activeorder")
        else:
            return redirect(url_for('homepage', error='true', **request.args))
    else:
        return render_template("errorViews/403.html")


def deleteParticipation(orderId):
    if session['role'] == 'student':
        studentId = session['id']
        order = getActiveOrder(orderId)
        if order and deleteParticipant(studentId, orderId):
            return redirect("/homepage")
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


def sendOrder(orderId):
    if session['role'] == 'student':
        order = getActiveOrder(orderId)
        if order and sendOrderContent(orderId):
            return redirect(url_for('homepage', ordered='true', **request.args))
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")
