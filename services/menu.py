import psycopg2 as dbapi2
from flask import current_app

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

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

def getAllMenusByRestaurantId(restaurantId):
  menus = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from menu where (restaurantid = %s)"
      cursor.execute(query,(restaurantId,))
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      if cursor.rowcount > 0:
          for i in cursor:
              menus.append(dict(zip(columns, i)))
          return menus
      else:
          return None