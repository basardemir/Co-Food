import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"

def deleteServiceById(serviceId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from service where (id=%s)"
                cursor.execute(query, (serviceId,))
                return True
    except:
        return False


def getServiceById(serviceId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from service where (id=%s)"
            cursor.execute(query, (serviceId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                service = dict(zip(columns, cursor.fetchone()))
                return service
            else:
                return None


def getServiceByRestaurantUniversity(restaurantId, universityId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from service where (service.universityid=%s AND service.restaurantid=%s )"
            cursor.execute(query, (universityId, restaurantId))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                service = dict(zip(columns, cursor.fetchone()))
                return service
            else:
                return None


def addServiceByRestaurantUniversity(restaurantId, universityId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into service (universityid, restaurantid) values (%s,%s)"
                cursor.execute(query, (universityId, restaurantId))
                return True
    except:
        return False
