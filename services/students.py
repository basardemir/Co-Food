import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def getAllStudentsByUniId(uniId):
  students = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select username, email from student where (universityid = %s)"
      cursor.execute(query,(uniId,))
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      if cursor.rowcount > 0:
          for i in cursor:
            students.append(dict(zip(columns, i)))
          return students
      else:
          return None

