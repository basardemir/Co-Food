from flask import redirect
from flask import render_template
from flask_login.utils import *

from forms.menu import *
from services.menu import *
from services.restaurant import *


@login_required
def adminMenus():
    if session['role'] == 'admin':
        menus = getAllMenus()
        return render_template("adminViews/menus.html", menus=menus)
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteMenu(menuId):
    if session['role'] == 'admin':
        menu = getMenuById(menuId)
        if menu:
            deleteMenuById(menuId)
            return redirect("/admin/restaurant/edit/" + str(menu["restaurantid"]))
    else:
        return render_template("errorViews/403.html")

@login_required
def deleteOwnerMenu(menuId):
    if session['role'] == 'owner':
        menu = getMenuById(menuId)
        if menu and menu['restaurantid'] == session['id']:
            deleteMenuById(menuId)
            return redirect("/owner/restaurant/")
    else:
        return render_template("errorViews/403.html")

@login_required
def addMenu():
    if session['role'] == 'admin':
        form = MenuEditForm()
        return render_template("adminViews/addMenu.html", form=form)
    else:
        return render_template("errorViews/403.html")


@login_required
def addMenuToRestaurant(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = MenuEditForm()
            return render_template("adminViews/addMenu.html", form=form, restaurant=restaurant)
        else:
            # to be completed
            return render_template("adminViews/universities.html", message="This university does not exists")
    else:
        return render_template("errorViews/403.html")


@login_required
def addOwnerMenu():
    if session['role'] == 'owner':
        restaurantId = session['id']
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = MenuEditOwnerForm()
            return render_template("ownerViews/addMenu.html", form=form, restaurant=restaurant)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def editMenu(menuId):
    if session['role'] == 'admin':
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant:
            form = MenuEditForm()
            return render_template("adminViews/editMenu.html", form=form, restaurant=restaurant, menu=menu)
        else:
            # to be completed
            return render_template("adminViews/menus.html", message="This menu or restaurant does not exists")
    else:
        return render_template("errorViews/403.html")

@login_required
def editOwnerMenu(menuId):
    if session['role'] == 'owner':
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant and menu['restaurantid'] == session['id']:
            form = MenuEditOwnerForm()
            return render_template("ownerViews/editMenu.html", form=form, restaurant=restaurant, menu=menu)
        else:
            return render_template("errorViews/404.html")
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
            if (addMenuByRestaurantId(restaurantId, name, description, price, campaign) == True):
                return redirect("/admin/restaurant/edit/" + str(restaurantId))
        else:
            return render_template("errorViews/403.html")


@login_required
def insertOwnerMenu():
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'owner':
            restaurantId=session['id']
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            campaign = form.campaign.data
            if (addMenuByRestaurantId(restaurantId, name, description, price, campaign) == True):
                return redirect("/owner/restaurant/")
            else:
                return render_template("errorViews/404.html")
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
                restaurant = request.form['restaurant']
                description = request.form['description']
                campaign = form.campaign.data
                if (updateMenuById(menuId, name, description, price, campaign, restaurant) == True):
                    return redirect("/admin/restaurant/edit/" + str(restaurant))
        else:
            return render_template("errorViews/403.html")

@login_required
def saveOwnerMenu(menuId):
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'owner':
            menu = getMenuById(menuId)
            restaurant = getRestaurantById(menu['restaurantid'])
            if menu and restaurant and menu['restaurantid']==session['id']:
                name = request.form['name']
                price = request.form['price']
                description = request.form['description']
                campaign = form.campaign.data
                if (updateMenuById(menuId, name, description, price, campaign, menu['restaurantid'] ) == True):
                    return redirect("/owner/restaurant/" )
        else:
            return render_template("errorViews/403.html")