import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""


def getAllRestaurants():
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from restaurant left join category on (restaurant.categoryid = category.id) order by restaurant.id asc"
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
            query = "select * from restaurant left join category on (restaurant.categoryid = category.id) where(restaurant.id = %s) "
            cursor.execute(query, (restaurantId,))
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
            if name != "" and categoryId != '0':
                name = '%' + name + '%'
                query = "select * from restaurant join category on (restaurant.categoryid = category.id) where " \
                        "(restaurant.categoryid = %s AND LOWER(restaurant.name ) like LOWER(%s))  "
                cursor.execute(query, (categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select * from restaurant join category on (restaurant.categoryid = category.id) where " \
                        " (LOWER(restaurant.name ) like LOWER(%s))  "
                cursor.execute(query, (name,))
            elif categoryId != '0':
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


def deleteRestaurantById(restaurantId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from restaurant where (id=%s)"
                cursor.execute(query, (restaurantId,))
                return True
    except:
        return False


def getAllRestaurantsByCategoryId(catId):
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select name, email from restaurant where (categoryid = %s)"
            cursor.execute(query, (catId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    restaurants.append(dict(zip(columns, i)))
                return restaurants
            else:
                return None


def getRestaurantById(restaurantId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select *, restaurant.name as restaurantname, restaurant.id as restaurantId from restaurant left join category on (restaurant.categoryid = category.id) where (restaurant.id = %s) "
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            restaurant = dict(zip(columns, cursor.fetchone()))
            if restaurant:
                return restaurant
            else:
                return None


def editRestaurantById(restaurantId, name, categoryid):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                if categoryid != '0':
                    query = "update restaurant set name=%s, categoryid=%s where (id=%s)"
                    cursor.execute(query, (name, categoryid, restaurantId))
                else:
                    query = "update restaurant set name=%s, categoryid=NULL where (id=%s)"
                    cursor.execute(query, (name, restaurantId))
                return True
    except:
        return False
