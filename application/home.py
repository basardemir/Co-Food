from flask import Flask, render_template

def homepage():
    return render_template("consumerViews/main_page.html")