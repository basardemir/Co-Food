from flask import Flask, render_template
import psycopg2 as dbapi2

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main_page.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/restaurants')
def restaurants():
    return render_template("restaurants.html")

@app.route('/restaurant')
def restaurant():
    return render_template("restaurant.html")

@app.route('/campaigns')
def campaigns():
    return render_template("campaigns.html")

@app.route('/wait-room')
def wait_room():
    return render_template("wait_room.html")


if __name__ == '__main__':
    app.run()
