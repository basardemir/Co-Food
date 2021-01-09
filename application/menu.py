from flask import Flask, render_template
from services.restaurant import *
from services.menu import *
from services.university import *
from services.menu import *
from services.service import *
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from forms.restaurant import RestaurantEditForm
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

