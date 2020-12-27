from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login.utils import *


@login_required
def homepage():
    return render_template("consumerViews/main_page.html")
