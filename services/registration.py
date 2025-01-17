import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher


dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


def checkStudent(username, password):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select id from student where (student.username=%s AND student.password = %s)"
            cursor.execute(query, (username, password))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return None


def getStudent(username, password):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from student where (student.username=%s)"
            cursor.execute(query, (username,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                student = dict(zip(columns, cursor.fetchone()))
                if hasher.verify(password, student['password']):
                    return student
            else:
                return None


def getRestaurant(name, password):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from restaurant where (restaurant.name=%s)"
            cursor.execute(query, (name,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            try:
                if cursor.rowcount > 0:
                    restaurant = dict(zip(columns, cursor.fetchone()))
                    if hasher.verify(password, restaurant['password']):
                        return restaurant
                else:
                    return None
            except:
                return None


def getStudentById(Id):
    if Id == None:
        return None
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from student where (student.id=%s)"
            cursor.execute(query, (Id,))
            if cursor.rowcount > 0:
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                student = dict(zip(columns, cursor.fetchone()))
                return student
            else:
                return None


def getRestaurantById(id):
    if id == None:
        return None
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from restaurant where (restaurant.id=%s)"
            cursor.execute(query, (id,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            restaurant = dict(zip(columns, cursor.fetchone()))
            if restaurant:
                return restaurant
            else:
                return None


def addStudent(user):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into student(username, password, email, universityid) VALUES (%s,%s,%s,%s)"
                cursor.execute(query, user)
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail



def addRestaurant(user):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into restaurant(name, password, email, phonenumber) VALUES (%s,%s,%s,%s)"
                cursor.execute(query, user)
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail