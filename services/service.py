import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""


def deleteServiceById(serviceId):
  try:
    with dbapi2.connect(dsn) as connection:
      with connection.cursor() as cursor:
        query = "delete from service where (id=%s)"
        cursor.execute(query,(serviceId,))
        return True
  except:
    return False

def getServiceById(serviceId):
    with dbapi2.connect(dsn) as connection:
      with connection.cursor() as cursor:
        query = "select * from service where (id=%s)"
        cursor.execute(query,(serviceId,))
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
        cursor.execute(query,(universityId,restaurantId))
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
            cursor.execute(query,(universityId,restaurantId))
            return True
    except:
        return False