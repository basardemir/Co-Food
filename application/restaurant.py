from services.restaurant import *
from flask import redirect, session
from flask import render_template, request
from flask_login.utils import *

from forms.comment import *
from forms.filter import RestaurantSearchForm
from forms.restaurant import RestaurantEditForm
from services.comment import *
from services.menu import *
from services.restaurant import *
from services.service import *
from services.students import getStudentDetail
from services.university import *


@login_required
def getRestaurants():
    if session['role'] == 'student':
        student = getStudentDetail(session['id'])
        university = student['universityid']
        restaurants = getAllRestaurantsWithUniversity(university)
        popularRestaurant = getMostPopularRestaurants()
        form = RestaurantSearchForm()
        return render_template("consumerViews/restaurants.html", popularRestaurants=popularRestaurant, form=form,
                               restaurants=restaurants)
    else:
        return render_template("errorViews/403.html")


@login_required
def filterRestaurants():
    if session['role'] == 'student':
        form = RestaurantSearchForm()
        student = getStudentDetail(session['id'])
        university = student['universityid']
        popularRestaurant = getMostPopularRestaurants()
        restaurants = filterRestaurant(request.form['restaurantname'], request.form['categories'],university)
        return render_template("consumerViews/restaurants.html", popularRestaurants=popularRestaurant, form=form,
                               restaurants=restaurants)
    else:
        return render_template("errorViews/403.html")


@login_required
def restaurant_details(restaurantId):
    if session['role'] == 'student' and isServesToStudent(session['id'],restaurantId):
        menus = getMenu(restaurantId)
        comments = getAllCommentsByRestaurantIdwithStudents(restaurantId)
        restaurant = getRestaurant(restaurantId)
        commentForm = CommentAddForm()
        popularMenus = getMostPopularMenusByRestaurantId(restaurantId)
        campaigns = []
        for menu in menus:
            if menu['iscampaign']:
                campaigns.append(menu)
                menus.remove(menu)
        information = {
            'restaurant': restaurant,
            'menus': menus,
            'campaigns': campaigns
        }
        return render_template("consumerViews/restaurant.html", popularmenus=popularMenus, comments=comments,
                               restaurant_info=information,
                               commentform=commentForm)
    else:
        return render_template("errorViews/403.html")


@login_required
def add_comment(restaurantId):
    if session['role'] == 'student' and isServesToStudent(session['id'],restaurantId):
        form = CommentAddForm()
        if form.validate_on_submit():
            description = request.form['comment']
            rate = request.form['rate']
            if (addComment(restaurantId, session['id'], description, rate)):
                menus = getMenu(restaurantId)
                restaurant = getRestaurant(restaurantId)
                commentForm = CommentAddForm()
                comments = getAllCommentsByRestaurantIdwithStudents(restaurantId)
                popularMenus = getMostPopularMenusByRestaurantId(restaurantId)
                information = {
                    'restaurant': restaurant,
                    'menus': menus
                }
                return render_template("consumerViews/restaurant.html", popularmenus=popularMenus, comments=comments,
                                       restaurant_info=information,
                                       commentform=commentForm)
    else:
        return render_template("errorViews/403.html")

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
def editRestaurant(restaurantId=0):
    if session['role'] == 'admin':
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = RestaurantEditForm()
            menus = getAllMenusByRestaurantId(restaurantId)
            universities = getAllUniversitiesByRestaurantId(restaurantId)
            comments = getAllCommentsByRestaurantId(restaurantId)
            return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                   comments=comments,
                                   universities=universities, menus=menus)
        else:
            restaurants = getAllRestaurants()
            return render_template("adminViews/restaurants.html", restaurants=restaurants,
                                   message="This restaurant does not exists.")
    if session['role'] == 'owner':
        restaurantId = session['id']
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = RestaurantEditForm()
            menus = getAllMenusByRestaurantId(restaurantId)
            universities = getAllUniversitiesByRestaurantId(restaurantId)
            comments = getAllCommentsByRestaurantId(restaurantId)
            return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                   comments=comments,
                                   universities=universities, menus=menus)
        else:
            restaurants = getAllRestaurants()
            return render_template("adminViews/restaurants.html", restaurants=restaurants,
                                   message="This restaurant does not exists.")
    else:
        return render_template("errorViews/403.html")


@login_required
def editOwnerRestaurant():
    if session['role'] == 'owner':
        restaurantId = session['id']
        restaurant = getRestaurantById(restaurantId)
        if restaurant:
            form = RestaurantEditForm()
            menus = getAllMenusByRestaurantId(restaurantId)
            universities = getAllUniversitiesByRestaurantId(restaurantId)
            comments = getAllCommentsByRestaurantId(restaurantId)
            return render_template("ownerViews/editRestaurant.html", form=form, restaurant=restaurant,
                                   comments=comments,
                                   universities=universities, menus=menus)
        return render_template("errorViews/404.html")
    else:
        return render_template("errorViews/403.html")


@login_required
def saveRestaurant(restaurantId):
    form = RestaurantEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            category = request.form['category']
            university = request.form['university']
            phone = request.form['phone']
            pdf = ''
            if form.menupdf.data:
                pdf = request.files[form.menupdf.name]
                if pdf.mimetype == 'application/pdf':
                    pdf = pdf.read()
                else:
                    restaurant = getRestaurantById(restaurantId)
                    menus = getAllMenusByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus, message="Input format only can "
                                                                                           "be only pdf.")
            if (editRestaurantById(restaurantId, name, category,phone) == True and (
                    addService(restaurantId, university) == True)):
                if pdf:
                    insertPdfToRestaurant(restaurantId, pdf)
                restaurant = getRestaurantById(restaurantId)
                if restaurant:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus)
                else:
                    restaurants = getAllRestaurants()
                    return render_template("adminViews/restaurants.html", restaurants=restaurants,
                                           message="This restaurant does not exists.")
            else:
                university = getUniversityById(restaurantId)
                restaurant = getRestaurantById(restaurantId)
                if university:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus, message="This name already exists")
                else:
                    restaurants = getAllRestaurants()
                    return render_template("adminViews/restaurants.html", restaurants=restaurants
                                           , message="This restaurant does not exists")
        else:
            return render_template("errorViews/403.html")
    restaurant = getRestaurantById(restaurantId)
    menus = getAllMenusByRestaurantId(restaurantId)
    universities = getAllUniversitiesByRestaurantId(restaurantId)
    comments = getAllCommentsByRestaurantId(restaurantId)
    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                           comments=comments,
                           universities=universities, menus=menus)


@login_required
def saveOwnerRestaurant():
    form = RestaurantEditForm()
    restaurantId = session['id']
    if form.validate_on_submit():
        if session['role'] == 'owner':
            name = request.form['name']
            pdf = ''
            category = request.form['category']
            university = request.form['university']
            if form.menupdf.data:
                pdf = request.files[form.menupdf.name]
                if pdf.mimetype == 'application/pdf':
                    pdf = pdf.read()
                else:
                    form = RestaurantEditForm()
                    restaurant = getRestaurantById(restaurantId)
                    menus = getAllMenusByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    return render_template("adminViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus, message="Input format only can "
                                                                                           "be only pdf.")
            if (editRestaurantById(restaurantId, name, category) == True and (
                    addService(restaurantId, university) == True)):
                if pdf:
                    insertPdfToRestaurant(restaurantId, pdf)
                restaurant = getRestaurantById(restaurantId)
                if restaurant:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    return render_template("ownerViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus)
                else:
                    return render_template("errorViews/404.html")
            else:
                university = getUniversityById(restaurantId)
                restaurant = getRestaurantById(restaurantId)
                if university:
                    form = RestaurantEditForm()
                    menus = getAllMenusByRestaurantId(restaurantId)
                    universities = getAllUniversitiesByRestaurantId(restaurantId)
                    comments = getAllCommentsByRestaurantId(restaurantId)
                    return render_template("ownerViews/editRestaurant.html", form=form, restaurant=restaurant,
                                           comments=comments,
                                           universities=universities, menus=menus, message="This name already exists")
                else:
                    return render_template("errorViews/404.html")
        else:
            return render_template("errorViews/403.html")


@login_required
def deleteService(serviceId):
    if session['role'] == 'admin':
        service = getServiceById(serviceId)
        if service:
            deleteServiceById(serviceId)
            return redirect("/admin/restaurant/edit/" + str(service["restaurantid"]))
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteOwnerService(serviceId):
    if session['role'] == 'owner':
        service = getServiceById(serviceId)
        if service and service['restaurantid'] == session['id']:
            deleteServiceById(serviceId)
            return redirect("/owner/restaurant/")
    else:
        return render_template("errorViews/403.html")


@login_required
def addService(restaurantId, universityId):
    if session['role'] == 'admin' or (session['role'] == 'owner' and session['id'] == restaurantId):
        service = getServiceByRestaurantUniversity(restaurantId, universityId)
        if service:
            return True
        if not service:
            addServiceByRestaurantUniversity(restaurantId, universityId)
            return True
        return False
    else:
        return render_template("errorViews/403.html")


@login_required
def deleteComment(commentId):
    if session['role'] == 'admin':
        comment = getCommentById(commentId)
        if comment:
            deleteCommentById(commentId)
            return redirect("/admin/restaurant/edit/" + str(comment["restaurantid"]))
    else:
        return render_template("errorViews/403.html")
