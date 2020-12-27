import psycopg2 as dbapi2
from flask import current_app
from passlib.hash import pbkdf2_sha256 as hasher
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

def getStudent(username,password):
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from student where (student.username=%s)"
      cursor.execute(query,(username,))
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      if cursor:
          student = dict(zip(columns, cursor.fetchone()))
          if hasher.verify(password,student['password']):
            return student
      else:
          return None

def getStudentById(Id):
  if Id == None:
    return None
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from student where (student.id=%s)"
      cursor.execute(query,(Id,))
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      student = dict(zip(columns, cursor.fetchone()))
      if student:
          return student
      else:
          return None

def addStudent(user):
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "insert into student(username, password, email, universityid) VALUES (%s,%s,%s,%s)"
      cursor.execute(query,user)