from flask import Flask, render_template
from services.restaurant import *
from services.menu import getMenu

def getRestaurants():
    restaurants=getAllRestaurants()
    for i in restaurants:
        print(i)
    return render_template("consumerViews/restaurants.html", restaurants = restaurants)

def restaurant_details(restaurantId):
    menus = getMenu(restaurantId)
    restaurant = getRestaurant(restaurantId)
    information = {
        'restaurant': restaurant,
        'menus': menus
    }
    return render_template("consumerViews/restaurant.html", restaurant_info=information)
