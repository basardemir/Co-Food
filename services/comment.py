import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""
dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


def getAllCommentsByRestaurantId(restaurantId):
    comments = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from comment where (restaurantid=%s)"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    comment = dict(zip(columns, i))
                    comments.append(comment)
                return comments
            else:
                return None


def getAllCommentsByRestaurantIdwithStudents(restaurantId):
    comments = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select student.id, student.username, c.description, c.rate " \
                    "from student inner join comment c on " \
                    "student.id = c.studentid where (c.restaurantid=%s)"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    comment = dict(zip(columns, i))
                    comments.append(comment)
                return comments
            else:
                return None


def addComment(restaurantId, studentId, description, rate):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into comment (restaurantid, studentid,description,rate) values (%s,%s,%s,%s)"
                cursor.execute(query, (restaurantId, studentId, description, rate))
                return True
    except:
        return False


def deleteCommentById(commentId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from comment where (id=%s)"
                cursor.execute(query, (commentId,))
                return True
    except:
        return False


def getCommentById(commentId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from comment where (id=%s)"
            cursor.execute(query, (commentId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                comment = dict(zip(columns, cursor.fetchone()))
                return comment
            else:
                return None
