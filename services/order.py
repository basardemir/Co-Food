import psycopg2 as dbapi2
from flask import current_app

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def hasActiveOrder(studentId):
    with dbapi2.connect(dsn) as connection:
      with connection.cursor() as cursor:
        query = "select count (orderstudentmatching.id) from orderstudentmatching left join ordercontent o on " \
                "o.id = orderstudentmatching.ordercontentid where (studentid=%s AND o.deliverytime = NULL)"
        cursor.execute(query,(studentId,))
        columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
        if cursor.fetchone() > 0:
          return True
        else:
          return False


