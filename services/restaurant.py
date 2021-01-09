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

def filterRestaurant(name, categoryId):
    restaurant = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            if name != "" and categoryId !='0':
                name ='%'+name+'%'
                query = "select * from restaurant join category on (restaurant.categoryid = category.id) where " \
                        "(restaurant.categoryid = %s AND LOWER(restaurant.name ) like LOWER(%s))  "
                cursor.execute(query, (categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select * from restaurant join category on (restaurant.categoryid = category.id) where " \
                        " (LOWER(restaurant.name ) like LOWER(%s))  "
                cursor.execute(query, (name,))
            elif categoryId !='0':
                query = "select * from restaurant join category on (restaurant.categoryid = category.id) where " \
                        "(restaurant.categoryid = %s)  "
                cursor.execute(query, (categoryId,))
            else:
                query = "select * from restaurant join category on (restaurant.categoryid = category.id)"
                cursor.execute(query)
            for id, name, email, password, catId, categoryId, catname in cursor:
                element = []
                element.append(id)
                element.append(name)
                element.append(catname)
                restaurant.append(element)
    return restaurant
