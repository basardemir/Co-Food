from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256 as hasher

def homepage():
    return render_template("consumerViews/main_page.html")