from flask import Flask, render_template
from services.restaurant import *
from services.menu import getMenu
from flask_login.utils import *
from forms.filter import RestaurantSearchForm

@login_required
def getRestaurants():
    if session['role'] == 'student':
        restaurants = getAllRestaurants()
        form = RestaurantSearchForm()
        return render_template("consumerViews/restaurants.html", form=form, restaurants = restaurants)
    else:
        return render_template("errorViews/403.html")

@login_required
def filterRestaurants():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        restaurants=filterRestaurant(request.form['restaurantname'], request.form['categories'])
        return render_template("consumerViews/restaurants.html", form=form, restaurants = restaurants)
    else:
        return render_template("errorViews/403.html")


@login_required
def restaurant_details(restaurantId):
    if session['role'] == 'student':
        menus = getMenu(restaurantId)
        restaurant = getRestaurant(restaurantId)
        information = {
            'restaurant': restaurant,
            'menus': menus
        }
        return render_template("consumerViews/restaurant.html", restaurant_info=information)





