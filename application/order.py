from flask_login import login_required

from services.restaurant import *
from flask import redirect, url_for, session
from flask import render_template, request

from forms.order import *
from services.menu import *
from services.order import *
from services.restaurant import *


def orderPage(menuId):
    if session['role'] == 'student':
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant and (isServesToStudent(session['id'], restaurant['restaurantid'])):
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
                success = request.args.get('success')
                if success == 'true':
                    return render_template("consumerViews/wait_room.html", success=True,order=order, friends=friends,
                                       friendsize=friendsize)
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
                if menu and restaurant and isServesToStudent(session['id'], restaurant['restaurantid']):
                    form = orderForm()
                    return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                                           form=form, message="You have non-delivered order.")
                else:
                    return render_template("errorViews/404.html")
            else:
                insertion = insertOrderSQL(menuId, session['id'], int(request.form['friendnumber']) + 1,
                                       request.form['ordercount'],
                                       request.form['address'])
                if (insertion != True):
                    form = orderForm()
                    menu = getMenuById(menuId)
                    restaurant = getRestaurantById(menu['restaurantid'])
                    return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                                           form=form, message= insertion+" An error occurred, try again!")
                else:
                    return redirect(url_for("activeOrder", success='true'))
        else:
            menu = getMenuById(menuId)
            restaurant = getRestaurantById(menu['restaurantid'])
            if menu and restaurant and (isServesToStudent(session['id'], restaurant['restaurantid'])):
                return render_template("consumerViews/order.html", menu=menu, restaurant=restaurant,
                                       form=form)
            else:
                return render_template("errorViews/404.html")
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
            return redirect(url_for('homepage', cancel='true', **request.args))
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


@login_required
def adminOrders():
    if session['role'] == 'admin':
        orders = getAllPastOrders()
        return render_template("adminViews/orders.html", orders=orders)
    else:
        return render_template("errorViews/403.html")


@login_required
def ownerOrders():
    if session['role'] == 'owner':
        restaurant_id = session['id']
        orders = getAllPastOrdersWithRestaurantId(restaurant_id)
        return render_template("ownerViews/orders.html", orders=orders)
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteOrder(orderId):
    if session['role'] == 'admin':
        if (deleteOrderById(orderId)):
            orders = getAllPastOrders()
            return render_template("adminViews/orders.html", orders=orders)
        else:
            orders = getAllPastOrders()
            return render_template("adminViews/orders.html", orders=orders,
                                   message="You cannot delete this order")
    else:
        return render_template("errorViews/403.html")


@login_required
def editOrder(orderId):
    if session['role'] == 'admin':
        order = getOrdersByOrderId(orderId)
        if (order):
            form = orderEditForm()
            menus = getAllMenusDictionary()
            friends = getOrderFriends(orderId)
            friendsize = len(friends)
            return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus, friends=friends,
                                   friendsize=friendsize)
        else:
            orders = getAllPastOrders()
            return render_template("adminViews/orders.html", orders=orders,
                                   message="You cannot edit this order")
    else:
        return render_template("errorViews/403.html")


@login_required
def saveOrder(orderId):
    form = orderEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            address = request.form['address']
            menu = request.form['menu']
            student = request.form['student']
            friendnumber = request.form['friendnumber']
            ordercount = request.form['ordercount']
            friends = getOrderFriends(orderId)
            friendsize = len(friends)
            if int(friendsize) >= int(friendnumber) + 1:
                form = orderEditForm()
                order = getOrdersByOrderId(orderId)
                menus = getAllMenusDictionary()
                friends = getOrderFriends(orderId)
                friendsize = len(friends)
                return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus,
                                       friends=friends, friendsize=friendsize,
                                       message="There are enough available students!")
            menuId = getMenuById(menu)
            if not menuId or not isServesToStudent(student, menuId['restaurantid']):
                form = orderEditForm()
                order = getOrdersByOrderId(orderId)
                menus = getAllMenusDictionary()
                friends = getOrderFriends(orderId)
                friendsize = len(friends)
                return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus,
                                       friends=friends, friendsize=friendsize,
                                       message="This student cannot takes service from menu's restaurant.")
            if hasActiveOrder(student):
                form = orderEditForm()
                order = getOrdersByOrderId(orderId)
                menus = getAllMenusDictionary()
                friends = getOrderFriends(orderId)
                friendsize = len(friends)
                return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus,
                                       friends=friends, friendsize=friendsize,
                                       message="This student has active order!")

            if (editOrderById(orderId, address, ordercount, int(friendnumber) + 1, menu) == True):
                if student is not '0':
                    if addMatchingByStudentOrder(student, orderId) == True:
                        return redirect('/admin/order/edit/' + str(orderId))
                    else:
                        form = orderEditForm()
                        order = getOrdersByOrderId(orderId)
                        menus = getAllMenusDictionary()
                        friends = getOrderFriends(orderId)
                        friendsize = len(friends)
                        return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus,
                                               friends=friends, friendsize=friendsize, message="Error occured!")
                else:
                    return redirect('/admin/order/edit/' + str(orderId))
            else:
                form = orderEditForm()
                order = getOrdersByOrderId(orderId)
                menus = getAllMenusDictionary()
                friends = getOrderFriends(orderId)
                friendsize = len(friends)
                return render_template("adminViews/editOrder.html", order=order, form=form, menus=menus,
                                       friends=friends, friendsize=friendsize, message="Error occured!")
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteMatching(matchId):
    if session['role'] == 'admin':
        match = getMatchById(matchId)
        if match:
            deleteMatchById(matchId)
            return redirect("/admin/order/edit/" + str(match["ordercontentid"]))
    else:
        return render_template("errorViews/403.html")


@login_required
def addOrder():
    if session['role'] == 'admin':
        form = orderAddForm()
        menus = getAllMenusDictionary()
        return render_template("adminViews/addOrder.html", form=form, menus=menus)
    else:
        return render_template("errorViews/403.html")


@login_required
def insertOrder():
    form = orderEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            address = request.form['address']
            menu = request.form['menu']
            student = request.form['student']
            friendnumber = request.form['friendnumber']
            ordercount = request.form['ordercount']

            if hasActiveOrder(student):
                form = orderAddForm()
                menus = getAllMenusDictionary()
                return render_template("adminViews/addOrder.html", form=form, menus=menus,
                                       message="This student has active order!")
            menuId = getMenuById(menu)
            if not menu or not isServesToStudent(student, menuId['restaurantid']):
                form = orderAddForm()
                menus = getAllMenusDictionary()
                return render_template("adminViews/addOrder.html", form=form, menus=menus,
                                       message="This student cannot takes service from menu's restaurant.")
            orderId = addOrderById(address, ordercount, int(friendnumber) + 1, menu)
            if orderId:
                if addMatchingByStudentOrder(student, orderId) == True:
                    return redirect('/admin/order/edit/' + str(orderId))
                else:
                    form = orderEditForm()
                    order = getOrdersByOrderId(orderId)
                    menus = getAllMenusDictionary()
                    friends = getOrderFriends(orderId)
                    return render_template("adminViews/editOrder.html", order=order, form=form, friends=friends,
                                           menus=menus, message="Student cannot be inserted.")
            else:
                form = orderAddForm()
                menus = getAllMenusDictionary()
                return render_template("adminViews/addOrder.html", form=form, menus=menus,
                                       message="This order cannot be inserted!")

    else:
        return render_template("errorViews/403.html")


def ownerOrderDetails(orderId):
    if session['role'] == 'owner':
        restaurantId = session['id']
        order = getOrderDetailsByOrderId(orderId)
        if order and order['restaurantid'] == session['id']:
            friends = getOrderFriends(order['id'])
            if friends:
                friendsize = len(friends)
                return render_template("ownerViews/orderDetails.html", order=order, friends=friends,
                                       friendsize=friendsize)
        return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")
