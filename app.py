from flask import Flask, render_template, current_app, request
import psycopg2 as dbapi2

app = Flask(__name__)

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""



def getRestaurants():
  restaurants = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from restaurant join category on (restaurant.categoryid = category.id)"
      cursor.execute(query)
      for id, name, email, password, catId, categoryId, catname in cursor:
          element = []
          element.append(id)
          element.append(name)
          element.append(catname)
          restaurants.append(element)
  return restaurants


def getMenu(restaurantId):
  menus = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from menu where(restaurantid = %s)"
      cursor.execute(query,(restaurantId,))
      for el in cursor:
          element = []
          element.append(el[1])
          element.append(el[2])
          element.append(el[3])
          menus.append(element)
  return menus

def getRestaurant(restaurantId):
    restaurant = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from restaurant join category on (restaurant.categoryid = category.id) where(restaurant.id = %s) "
            cursor.execute(query,(restaurantId,))
            for id, name, email, password, catId, categoryId, catname in cursor:
                element = []
                element.append(id)
                element.append(name)
                element.append(catname)
                restaurant.append(element)
    return restaurant

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
    restaurants=getRestaurants()
    for i in restaurants:
        print(i)
    return render_template("consumerViews/restaurants.html", restaurants = restaurants)

@app.route('/restaurant')
def restaurant():
    restaurantId = request.args.get('restaurantId', type=int)
    menus = getMenu(restaurantId)
    restaurant = getRestaurant(restaurantId)
    information = {
        'restaurant':restaurant,
        'menus': menus
    }

    print(menus)
    return render_template("consumerViews/restaurant.html", restaurant_info = information)

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
