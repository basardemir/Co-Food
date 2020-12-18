from flask import Flask, render_template
import psycopg2 as dbapi2

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("consumerViews/main_page.html")


@app.route('/register')
def register():
    return render_template("consumerViews/register.html")

@app.route('/login')
def login():
    return render_template("consumerViews/login.html")

@app.route('/restaurants')
def restaurants():
    return render_template("consumerViews/restaurants.html")

@app.route('/restaurant')
def restaurant():
    return render_template("consumerViews/restaurant.html")

@app.route('/campaigns')
def campaigns():
    return render_template("consumerViews/campaigns.html")

@app.route('/wait-room')
def wait_room():
    return render_template("consumerViews/wait_room.html")

@app.route('/order')
def order():
    return render_template("consumerViews/order.html")

@app.route('/settings')
def settingsView():
    return render_template("consumerViews/settings.html")

@app.route('/history')
def historyView():
    return render_template("consumerViews/history.html")


if __name__ == '__main__':
    app.run()
