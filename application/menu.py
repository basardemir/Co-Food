from io import BytesIO

from flask import redirect, send_file
from flask import render_template
from flask_login.utils import *

from application.restaurant import editOwnerRestaurant
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
        count = isMenuActive(menuId)
        if menu and count==0:
            try:
                deleteMenuById(menuId)
            except:
                return redirect("/admin/restaurant/edit/" + str(menu["restaurantid"]) + '?error=true')
            return redirect("/admin/restaurant/edit/" + str(menu["restaurantid"]) + '?success=true')
        else:
            return redirect("/admin/restaurant/edit/" + str(menu["restaurantid"]) + '?menuerror="true"')
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteOwnerMenu(menuId):
    if session['role'] == 'owner':
        menu = getMenuById(menuId)
        count = isMenuActive(menuId)
        if menu and menu['restaurantid'] == session['id'] and count==0:
            try:
                deleteMenuById(menuId)
            except:
                return redirect(url_for("editOwnerRestaurant", error="true"))
            return redirect(url_for("editOwnerRestaurant", success="true"))
        else:
            return redirect(url_for("editOwnerRestaurant", menuerror="true"))
    else:
        return render_template("errorViews/403.html")


@login_required
def addMenu():
    if session['role'] == 'admin':
        form = MenuEditForm()
        form.restaurant.choices=getAllRestaurantsForm()
        return render_template("adminViews/addMenu.html", form=form)
    else:
        return render_template("errorViews/403.html")


@login_required
def addMenuToRestaurant(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = MenuEditForm()
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("adminViews/addMenu.html", form=form, restaurant=restaurant)
        else:
            return redirect("adminViews/restaurants")
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
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("adminViews/editMenu.html", form=form, restaurant=restaurant, menu=menu)
        else:
            return redirect("adminViews/menus.html")
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
            ingredients = request.form['ingredients']
            campaign = form.campaign.data
            if (addMenuByRestaurantId(restaurantId, name, description, price, campaign, ingredients) == True):
                return redirect("/admin/restaurant/edit/" + str(restaurantId) + "?success=true")
            else:
                restaurant = getRestaurantById(restaurantId)
                if restaurant:
                    form.restaurant.choices = getAllRestaurantsForm()
                    return render_template("adminViews/addMenu.html", form=form, restaurant=restaurant,
                                           message="An error occured")
                else:
                    return render_template("errorViews/404.html")
        else:
            return render_template("errorViews/403.html")
    else:
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("adminViews/addMenu.html", form=form, restaurant=restaurant)
        else:
            return render_template("errorViews/404.html")


@login_required
def createMenu():
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            restaurant = request.form['restaurant']
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            ingredients = request.form['ingredients']
            campaign = form.campaign.data
            if (addMenuByRestaurantId(restaurant, name, description, price, campaign, ingredients) == True):
                return redirect("/admin/restaurant/edit/" + str(restaurant))
            else:
                return redirect("/admin/restaurant/edit/" + str(restaurant)+'?error=true')
        else:
            return render_template("errorViews/403.html")
    else:
        form.restaurant.choices=getAllRestaurantsForm()
        return render_template("adminViews/addMenu.html", form=form)


@login_required
def insertOwnerMenu():
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'owner':
            restaurantId = session['id']
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            ingredients = request.form['ingredients']
            campaign = form.campaign.data
            addMenu = addMenuByRestaurantId(restaurantId, name, description, price, campaign, ingredients)
            if (addMenu == True):
                return redirect(url_for("editOwnerRestaurant", success="true"))
            else:
                return redirect(url_for("editOwnerRestaurant", error="true"))
        else:
            return render_template("errorViews/403.html")
    else:
        restaurantId = session['id']
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("ownerViews/addMenu.html", form=form, restaurant=restaurant)
        else:
            return render_template("errorViews/404.html")


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
                ingredients = request.form['ingredients']
                campaign = form.campaign.data
                if (updateMenuById(menuId, name, description, price, campaign, restaurant, ingredients) == True):
                    return redirect("/admin/restaurant/edit/" + str(restaurant) + '?success=true')
                else:
                    menu = getMenuById(menuId)
                    restaurant = getRestaurantById(menu['restaurantid'])
                    if menu and restaurant:
                        form = MenuEditForm()
                        form.restaurant.choices = getAllRestaurantsForm()
                        return render_template("adminViews/editMenu.html", form=form, restaurant=restaurant, menu=menu
                                               ,message="An error occured")
                    else:
                        return render_template("adminViews/menus.html",
                                               message="This menu or restaurant does not exists")
        else:
            return render_template("errorViews/403.html")
    else:
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant:
            form = MenuEditForm()
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("adminViews/editMenu.html", form=form, restaurant=restaurant, menu=menu)
        else:
            return render_template("adminViews/menus.html", message="This menu or restaurant does not exists")


@login_required
def saveOwnerMenu(menuId):
    form = MenuEditForm()
    if form.validate_on_submit():
        if session['role'] == 'owner':
            menu = getMenuById(menuId)
            restaurant = getRestaurantById(menu['restaurantid'])
            if menu and restaurant and menu['restaurantid'] == session['id']:
                name = request.form['name']
                price = request.form['price']
                description = request.form['description']
                ingredients = request.form['ingredients']
                campaign = form.campaign.data
                updateMenu = updateMenuById(menuId, name, description, price, campaign, menu['restaurantid'],
                                            ingredients)
                if (updateMenu == True):
                    return redirect(url_for("editOwnerRestaurant", success="true"))
                else:
                    return redirect(url_for("editOwnerRestaurant", error="true"))
            else:
                return render_template("errorViews/403.html")
        else:
            return render_template("errorViews/403.html")

    else:
        menu = getMenuById(menuId)
        restaurant = getRestaurantById(menu['restaurantid'])
        if menu and restaurant and session['role'] == 'owner' and menu['restaurantid'] == session['id']:
            form.restaurant.choices = getAllRestaurantsForm()
            return render_template("ownerViews/editMenu.html", form=form, restaurant=restaurant, menu=menu)
        else:
            return render_template("errorViews/403.html")


@login_required
def downloadMenuPdf(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant['menupdf']:
            data = restaurant['menupdf']
            return send_file(BytesIO(data), attachment_filename=restaurant['restaurantname'] + 'menu.pdf', as_attachment=True)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteMenuPdf(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant and restaurant['menupdf']:
            deletePdfFromRestaurant(restaurantId)
            return redirect("/admin/restaurant/edit/" + str(restaurantId))
        else:
            return render_template("errorViews/403.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def downloadOwnerMenuPdf(restaurantId):
    restaurant = getRestaurantById(restaurantId)
    if session['role'] == 'owner' and restaurant and restaurant['restaurantid'] == session['id']:
        if restaurant['menupdf']:
            data = restaurant['menupdf']
            return send_file(BytesIO(data), attachment_filename=restaurant['restaurantname'] + 'menu.pdf', as_attachment=True)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def downloadStudentMenuPdf(restaurantId):
    restaurant = getRestaurantById(restaurantId)
    if session['role'] == 'student' and restaurant:
        if restaurant['menupdf']:
            data = restaurant['menupdf']
            return send_file(BytesIO(data), attachment_filename=restaurant['restaurantname'] + 'menu.pdf', as_attachment=True)
        else:
            return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteOwnerMenuPdf(restaurantId):
    restaurant = getRestaurantById(restaurantId)
    if session['role'] == 'owner' and restaurant and restaurant['restaurantid'] == session['id']:
        if restaurant and restaurant['menupdf']:
            deletePdfFromRestaurant(restaurantId)
            return redirect("/owner/restaurant/")
        else:
            return render_template("errorViews/403.html")
    else:
        return render_template("errorViews/403.html")
