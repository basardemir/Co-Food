import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""
dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


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


def addMenuByRestaurantId(restaurantId, name, description, price, campaign,ingredients):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into menu (name, description,price,iscampaign, restaurantid,ingredients) values (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (name, description, price, campaign, restaurantId,ingredients))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail


def updateMenuById(menuId, name, description, price, campaign, restaurant,ingredients):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update menu set name=%s, description=%s,price=%s,iscampaign=%s, restaurantid=%s,ingredients=%s where(id=%s)"
                cursor.execute(query, (name, description, price, campaign, restaurant,ingredients, menuId))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail


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

def getAllMenusDictionary():
    menus = {}
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select menu.name as name, price,description,restaurant.name as restaurantname, menu.id as id from menu left join restaurant on (restaurant.id = menu.restaurantid) order by menu.name asc"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    menu = dict(zip(columns, i))
                    menus[menu['id']] = menu
                return menus
            else:
                return None

def getAllMenusForm():
    menus = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select id,name from menu order by name asc"
            cursor.execute(query)
            for i in cursor:
                menus.append((i[0], i[1]))
    return menus
