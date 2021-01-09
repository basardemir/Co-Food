from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.university import *
from services.menu import *
from services.service import *
from flask_login.utils import *
from forms.menu import *
from flask import redirect, url_for



@login_required
def deleteMenu(menuId):
    if session['role'] == 'admin':
        menu = getMenuById(menuId)
        if menu:
            deleteMenuById(menuId)
            return redirect("/admin/restaurant/edit/"+str(menu["restaurantid"]))
    else:
        return render_template("errorViews/403.html")

@login_required
def addMenu(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = MenuEditForm()
            return render_template("adminViews/addMenu.html", form = form, restaurant=restaurant)
        else:
            #to be completed
            return render_template("adminViews/universities.html", message="This university does not exists")
    else:
        return render_template("errorViews/403.html")

@login_required
def editMenu(menuId):
    if session['role'] == 'admin':
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant:
            form = MenuEditForm()
            return render_template("adminViews/editMenu.html", form = form, restaurant=restaurant, menu=menu)
        else:
            #to be completed
            return render_template("adminViews/universities.html", message="This university does not exists")
    else:
        return render_template("errorViews/403.html")


@login_required
def insertMenu(restaurantId):
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            campaign = form.campaign.data
            if (addMenuByRestaurantId(restaurantId, name,description,price,campaign) == True):
                return redirect("/admin/restaurant/edit/" + str(restaurantId))
        else:
            return render_template("errorViews/403.html")

@login_required
def saveMenu(menuId):
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            menu = getMenuById(menuId)
            restaurant = getRestaurantById(menu['restaurantid'])
            if menu and restaurant:
                name = request.form['name']
                price = request.form['price']
                description = request.form['description']
                campaign = form.campaign.data
                if (updateMenuById(menuId,name, description, price, campaign) == True):
                    return redirect("/admin/restaurant/edit/" + str(menu['restaurantid']))
        else:
            return render_template("errorViews/403.html")