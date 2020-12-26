import psycopg2 as dbapi2
from flask import current_app

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def checkStudent(username,password):
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select id from student where (student.username=%s AND student.password = %s)"
      cursor.execute(query,(username,password))
      data = cursor.fetchone()
      if data:
          return data[0]
      else:
          return None

def addStudent(user):
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "insert into student(username, password, email, universityid) VALUES (%s,%s,%s,%s)"
      cursor.execute(query,user)