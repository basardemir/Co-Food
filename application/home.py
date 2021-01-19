import datetime
from time import strptime

from flask import render_template
from flask_login.utils import *

from forms.filter import RestaurantSearchForm
from services.order import *
from services.restaurant import *
from services.students import *


@login_required
def homepage():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        student = getStudentDetail(session['id'])
        university = student['universityid']
        orders = getAllOrdersWithUniversityId(university)
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
        cancel = request.args.get('cancel')
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
        if cancel == 'true':
            return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                                   form=form, students=students, orders=orders,
                                   cancel='true')
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
        if form.validate_on_submit():
            form = RestaurantSearchForm()
            students = getMostOrderingStudents()
            student = getStudentDetail(session['id'])
            university = student['universityid']
            orders = getAllOrdersWithFilter(request.form['restaurantname'], request.form['categories'], university)
            return render_template("consumerViews/main_page.html", form=form, students=students, orders=orders)
        else:
            student = getStudentDetail(session['id'])
            students = getMostOrderingStudents()
            university = student['universityid']
            ordercount = getNumberofDeliveredOrders()
            orders = getAllOrdersWithUniversityId(university)
            average_time = getAverageDeliverTime()
            return render_template("consumerViews/main_page.html", ordercount=ordercount, averagetime=average_time,
                                   form=form, students=students, orders=orders)
    else:
        return render_template("errorViews/403.html")