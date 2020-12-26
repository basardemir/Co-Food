import psycopg2 as dbapi2
from flask import current_app

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def getAllRestaurants():
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