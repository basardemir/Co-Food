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

def getAllStudentsForm():
    students = []
    students.append((0, "Select"))
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select id,username from student order by username"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    students.append((i[0], i[1]))
                return students
            else:
                return None

def getAllStudentsAddForm():
    students = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select id,username from student order by username"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    students.append((i[0], i[1]))
                return students
            else:
                return None

def getStudentDetail(studentId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select username, email, universityid, password" \
                    " from student left join university u on student.universityid = u.id " \
                    "where (student.id=%s) "
            cursor.execute(query, (studentId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                student = dict(zip(columns, cursor.fetchone()))
                return student
            else:
                return None


def getUserHistory(userId):
    history = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select ordercontentid, menuid, restaurantid, r.name as restaurantname," \
                    "price, ordertime, m.name as menuname from orderstudentmatching left join ordercontent o on " \
                    "orderstudentmatching.ordercontentid = o.id left join menu m on m.id = o.menuid " \
                    "left join restaurant r on r.id = m.restaurantid where (studentid = %s AND o.isdelivered=TRUE) " \
                    "order by o.ordertime desc"
            cursor.execute(query, (userId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    history.append(dict(zip(columns, i)))
                return history
            else:
                return None


def updateUserWithPassword(userId, username, email, password, universityid):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update student set username=%s, email=%s,password=%s,universityid=%s where(id=%s)"
                cursor.execute(query, (username, email, password, universityid, userId))
                return True
    except:
        return False

def updateUserWithoutPassword(userId, username, email, universityid):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update student set username=%s, email=%s, universityid=%s where(id=%s)"
                cursor.execute(query, (username, email, universityid, userId))
                return True
    except:
        return False