from flask import Flask, render_template

def register():
    return render_template("consumerViews/register.html")

def login():
    return render_template("consumerViews/login.html")