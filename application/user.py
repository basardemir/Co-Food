from flask import Flask, render_template



def userSettings():
    return render_template("consumerViews/settings.html")

def userHistory():
    return render_template("consumerViews/history.html")


