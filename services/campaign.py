import psycopg2 as dbapi2
from flask import current_app

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def getAllCampaigns():
  campaigns = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from menu join restaurant on (restaurant.id = menu.restaurantid) where(menu.iscampaign = true)"
      cursor.execute(query)
      for i in cursor:
          element_dic = {
              "price":i[1],
              "name": i[2],
              "content": i[3],
              "restaurantId": i[5],
              "restaurantName": i[7],
          }
          campaigns.append(element_dic)
  return campaigns