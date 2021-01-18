import datetime
from time import strptime

from flask import render_template
from flask_login.utils import *

from forms.filter import RestaurantSearchForm
from services.order import *
from services.restaurant import *


@login_required
def homepage():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        orders = getAllOrders()
        average_time = getAverageDeliverTime()
        if not average_time:
            average_time = 0
        else:
            average_time = str(datetime.timedelta(seconds=average_time['averagetime'].seconds))
        ordercount = getNumberofDeliveredOrders()
        if ordercount:
            ordercount = ordercount['ordercount']
        else:
            ordercount = 0
        notactive = request.args.get('noactiveorder')
        ordered = request.args.get('ordered')
        error = request.args.get('error')
        students = getMostOrderingStudents()
        if orders:
            for i in orders:
                i['friendnumber'] = len(getOrderFriends(i['id']))
        if notactive:
            return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                                   form=form, students=students, orders=orders,
                                   noactiveorder='true')
        if ordered == 'true':
            return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                                   form=form, students=students, orders=orders,
                                   ordered='true')
        if error == 'true':
            return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                                   form=form, students=students, orders=orders,
                                   error='true')
        return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                               form=form, students=students, orders=orders)
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
    form = RestaurantSearchForm()
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        mostPopularRestaurants = getMostPopularRestaurants()
        students = getMostOrderingStudents()
        orders = getAllOrdersWithFilter(request.form['restaurantname'], request.form['categories'])
        return render_template("consumerViews/main_page.html", form=form, students=students, orders=orders)
    else:
        return render_template("errorViews/403.html")
