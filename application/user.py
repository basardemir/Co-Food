from flask import render_template
from flask import render_template
from flask import session

from services.order import *
from services.students import *


def userSettings():
    return render_template("consumerViews/settings.html")


def userHistory():
    if session['role'] == 'student':
        userId = session['id']
        history = getUserHistory(userId)
        orderfriends = {}
        for i in range(len(history)):
            orderfriends[str(history[i]['ordercontentid'])] = getOrderFriends(history[i]['ordercontentid'])
        return render_template("consumerViews/history.html", history=history, friends=orderfriends)
    else:
        return render_template("errorViews/403.html")
