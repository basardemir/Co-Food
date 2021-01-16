import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""


def getMenu(restaurantId):
    menus = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from menu where(restaurantid = %s)"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    menus.append(dict(zip(columns, i)))
                return menus
            else:
                return None


def getAllMenusByRestaurantId(restaurantId):
    menus = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from menu where (restaurantid = %s)"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    menus.append(dict(zip(columns, i)))
                return menus
            else:
                return None


def getMenuById(menuId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from menu where (id=%s)"
            cursor.execute(query, (menuId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                menu = dict(zip(columns, cursor.fetchone()))
                return menu
            else:
                return None


def deleteMenuById(menuId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from menu where (id=%s)"
                cursor.execute(query, (menuId,))
                return True
    except:
        return False


def addMenuByRestaurantId(restaurantId, name, description, price, campaign):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into menu (name, description,price,iscampaign, restaurantid) values (%s,%s,%s,%s,%s)"
                cursor.execute(query, (name, description, price, campaign, restaurantId))
                return True
    except:
        return False


def updateMenuById(menuId, name, description, price, campaign, restaurant):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update menu set name=%s, description=%s,price=%s,iscampaign=%s, restaurantid=%s where(id=%s)"
                cursor.execute(query, (name, description, price, campaign, restaurant, menuId))
                return True
    except:
        return False


def getAllMenus():
    menus = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select menu.name as name, restaurant.name as restaurantname, menu.id as id from menu left join restaurant on (restaurant.id = menu.restaurantid) order by menu.name asc"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    menus.append(dict(zip(columns, i)))
                return menus
            else:
                return None
