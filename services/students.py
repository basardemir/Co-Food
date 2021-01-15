import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""


def getAllStudentsByUniId(uniId):
    students = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select username, email from student where (universityid = %s)"
            cursor.execute(query, (uniId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    students.append(dict(zip(columns, i)))
                return students
            else:
                return None


def getUserHistory(userId):
    history = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select ordercontentid, menuid, restaurantid, r.name as restaurantname," \
                    "price, ordertime, m.name as menuname from orderstudentmatching left join ordercontent o on " \
                    "orderstudentmatching.ordercontentid = o.id left join menu m on m.id = o.menuid " \
                    "left join restaurant r on r.id = m.restaurantid where (studentid = %s AND o.isdelivered=TRUE)"
            cursor.execute(query, (userId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    history.append(dict(zip(columns, i)))
                return history
            else:
                return None
