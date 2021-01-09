from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.university import *
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from forms.restaurant import RestaurantEditForm


@login_required
def getRestaurants():
    if session['role'] == 'student':
        restaurants = getAllRestaurants()
        form = RestaurantSearchForm()
        return render_template("consumerViews/restaurants.html", form=form, restaurants=restaurants)
    else:
        return render_template("errorViews/403.html")


@login_required
def filterRestaurants():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        restaurants = filterRestaurant(request.form['restaurantname'], request.form['categories'])
        return render_template("consumerViews/restaurants.html", form=form, restaurants=restaurants)
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


@login_required
def adminRestaurants():
    if session['role'] == 'admin':
        restaurants = getAllRestaurants()
        return render_template("adminViews/restaurants.html", restaurants=restaurants)
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteRestaurant(restaurantId):
    if session['role'] == 'admin':
        if (deleteRestaurantById(restaurantId)):
            restaurants = getAllRestaurants()
            return render_template("adminViews/restaurants.html", restaurants=restaurants)
        else:
            restaurants = getAllRestaurants()
            return render_template("adminViews/restaurants.html", restaurants=restaurants,
                                   message="You cannot delete this restaurant")
    else:
        return render_template("errorViews/403.html")


@login_required
def editRestaurant(restaurantId):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = RestaurantEditForm()
            menus = getAllMenusByRestaurantId(restaurantId)
            universities = getAllUniversitiesByRestaurantId(restaurantId)
            print(universities)
            print("dkjsnkdf")
            return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                   universities=universities, menus=menus)
        else:
            restaurants = getAllRestaurants()
            return render_template("adminViews/restaurants.html", restaurants=restaurants,
                                   message="This restaurant does not exists.")
    else:
        return render_template("errorViews/403.html")


@login_required
def saveRestaurant(restaurantId):
    form = RestaurantEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            category = request.form['category']
            if (editRestaurantById(restaurantId, name, category) == True):
                restaurant = getRestaurantById(restaurantId)
                if restaurant:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           universities=universities, menus=menus)
                else:
                    restaurants = getAllRestaurants()
                    return render_template("adminViews/restaurants.html", restaurants=restaurants,message="This restaurant does not exists.")
            else:
                university = getUniversityById(restaurantId)
                restaurant = getRestaurantById(restaurantId)
                if university:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           universities=universities, menus=menus, message="This name already exists")
                else:
                    restaurants = getAllRestaurants()
                    return render_template("adminViews/restaurants.html", restaurants=restaurants
                                           , message="This restaurant does not exists")
        else:
            return render_template("errorViews/403.html")
