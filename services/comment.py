import psycopg2 as dbapi2
from flask import current_app
from passlib.hash import pbkdf2_sha256 as hasher
dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""



def getAllCommentsByRestaurantId(restaurantId):
  comments = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from comment where (restaurantid=%s)"
      cursor.execute(query,(restaurantId,))
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
      cursor.execute(query,(restaurantId,))
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      if cursor.rowcount > 0:
          for i in cursor:
            comment = dict(zip(columns, i))
            comments.append(comment)
          return comments
      else:
          return None


def addComment(restaurantId,studentId, description,rate):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into comment (restaurantid, studentid,description,rate) values (%s,%s,%s,%s)"
                cursor.execute(query, (restaurantId,studentId, description,rate))
                return True
    except:
        return False