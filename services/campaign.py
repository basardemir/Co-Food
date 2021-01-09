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
                    "price": i[1],
                    "name": i[2],
                    "content": i[3],
                    "restaurantId": i[5],
                    "restaurantName": i[7],
                }
                campaigns.append(element_dic)
    return campaigns


def filterCampaign(name, categoryId):
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            if name != "" and categoryId != '0':
                name = '%' + name + '%'
                query = "select * from menu join restaurant on (restaurant.id = menu.restaurantid) where " \
                        "(menu.iscampaign = true AND restaurant.categoryid = %s AND LOWER(menu.name ) like LOWER(%s))  "
                cursor.execute(query, (categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select * from menu join restaurant on (menu.restaurantid = restaurant.id ) where " \
                        " (menu.iscampaign = true AND LOWER(menu.name ) like LOWER(%s))  "
                cursor.execute(query, (name,))
            elif categoryId != '0':
                query = "select * from menu join restaurant on (restaurant.categoryid = restaurant.id ) where " \
                        "(menu.iscampaign = true AND restaurant.categoryid = %s)  "
                cursor.execute(query, (categoryId,))
            else:
                query = "select * from menu join restaurant on (restaurant.id = menu.restaurantid) where(menu.iscampaign = true)"
                cursor.execute(query)
            for i in cursor:
                element_dic = {
                    "price": i[1],
                    "name": i[2],
                    "content": i[3],
                    "restaurantId": i[5],
                    "restaurantName": i[7],
                }
                campaigns.append(element_dic)
    return campaigns