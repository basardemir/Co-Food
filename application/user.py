from services.registration import *
from flask import render_template
from flask import render_template
from flask import session
from flask_login import login_required
from flask import current_app, flash, redirect, url_for, session
from flask import render_template, request
from flask_login import UserMixin, login_user, logout_user
from forms.settings import *
from services.order import *
from services.students import *
from services.restaurant import *


@login_required
def userSettings():
    if session['role'] == 'student':
        userId = session['id']
        user = getStudentDetail(userId)
        form = SettingsForm()
        return render_template("consumerViews/settings.html", user=user, form=form)
    else:
        return render_template("errorViews/403.html")


@login_required
def updateUser():
    if session['role'] == 'student':
        userId = session['id']
        form = SettingsForm()
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            university = request.form['university']
            if (hasActiveOrder(session['id'])):
                user = getStudentDetail(userId)
                form = SettingsForm()
                return render_template("consumerViews/settings.html", user=user, form=form,
                                       messages=["You have active order, you cannot change your information."])
            email = request.form['email']
            if form['passwordchange'].data == 'True':
                userUpdate = updateUserWithPassword(userId, username, hasher.hash(password), email, university)
                if userUpdate != True:
                    user = getStudentDetail(userId)
                    form = SettingsForm()
                    return render_template("consumerViews/settings.html", user=user, form=form, messages=[userUpdate])
                else:
                    user = getStudentDetail(userId)
                    form = SettingsForm()
                    return render_template("consumerViews/settings.html", user=user, form=form, success='true')
            else:
                userUpdate = updateUserWithoutPassword(userId, username, email, university)
                if userUpdate != True:
                    user = getStudentDetail(userId)
                    form = SettingsForm()
                    return render_template("consumerViews/settings.html", user=user, form=form, messages=[userUpdate])
                else:
                    user = getStudentDetail(userId)
                    form = SettingsForm()
                    return render_template("consumerViews/settings.html", user=user, form=form, success='true')
        else:
            userId = session['id']
            user = getStudentDetail(userId)
            return render_template("consumerViews/settings.html", user=user, form=form)
    else:
        return render_template("errorViews/403.html")


def userHistory():
    if session['role'] == 'student':
        userId = session['id']
        history = getUserHistory(userId)
        favoriteMenus = getMostPopularMenusByStudentId(userId)
        favoriteRestaurants = getMostPopularRestaurantsByStudentId(userId)
        orderfriends = {}
        if history:
            for i in range(len(history)):
                orderfriends[str(history[i]['ordercontentid'])] = getOrderFriends(history[i]['ordercontentid'])
            return render_template("consumerViews/history.html", restaurants=favoriteRestaurants, menus=favoriteMenus,
                                   history=history, friends=orderfriends)
        return render_template("consumerViews/history.html")
    else:
        return render_template("errorViews/403.html")
