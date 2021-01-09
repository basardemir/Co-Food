from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from services.category import *
from forms.category import *
from flask import Flask, render_template, request
from services.restaurant import *

@login_required
def adminCategories():
    if session['role'] == 'admin':
        categories = getAllCategories()
        return render_template("adminViews/categories.html", categories=categories)
    else:
        return render_template("errorViews/403.html")

@login_required
def deleteCategory(catId):
    if session['role'] == 'admin':
        if(deleteCategoryById(catId)):
            categories = getAllCategories()
            return render_template("adminViews/categories.html", categories=categories)
        else:
            categories = getAllCategories()
            return render_template("adminViews/categories.html", categories=categories, message="You cannot delete this category")
    else:
        return render_template("errorViews/403.html")

@login_required
def addCategory():
    if session['role'] == 'admin':
        form = CategoryEditForm()
        return render_template("adminViews/addCategory.html", form=form)
    else:
        return render_template("errorViews/403.html")

@login_required
def insertCategory():
    form = CategoryEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            if (addCategoryByName(name) == True):
                categories = getAllCategories()
                return render_template("adminViews/categories.html", categories=categories)
            else:
                form = CategoryEditForm()
                return render_template("adminViews/addCategory.html", form=form, message="This name is already exist")
        else:
            return render_template("errorViews/403.html")


@login_required
def editCategory(catId):
    if session['role'] == 'admin':
        category = getCategoryById(catId)
        if category:
            form = CategoryEditForm()
            restaurants = getAllRestaurantsByCategoryId(catId)
            return render_template("adminViews/editCategory.html", form = form, category=category, restaurants = restaurants)
        else:
            categories = getAllCategories()
            return render_template("adminViews/categories.html",categories=categories, message="This category does not exists")
    else:
        return render_template("errorViews/403.html")

@login_required
def saveCategory(catId):
    form = CategoryEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            if(editCategoryById(catId,name) == True):
                category = getCategoryById(catId)
                if category:
                    form = CategoryEditForm()
                    restaurants = getAllRestaurantsByCategoryId(catId)
                    return render_template("adminViews/editCategory.html", form = form, category=category, restaurants = restaurants)
                else:
                    categories = getAllCategories()
                    return render_template("adminViews/categories.html",categories=categories, message="This category does not exists")
            else:
                category = getCategoryById(catId)
                if category:
                    restaurants = getAllRestaurantsByCategoryId(catId)
                    form = CategoryEditForm()
                    return render_template("adminViews/editCategory.html", form=form, category=category,message="This name already exists", restaurants = restaurants)
                else:
                    categories = getAllCategories()
                    return render_template("adminViews/categories.html", categories=categories,
                                           message="This category does not exists")
        else:
            return render_template("errorViews/403.html")

