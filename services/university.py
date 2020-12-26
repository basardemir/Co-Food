import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

class University:
    def __init__(self,id,name):
        self.id=id
        self.name = name

def getAllUniversities():
  universities = []
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      query = "select * from university"
      cursor.execute(query)
      for i in cursor:
        universities.append(University(i[0],i[1]))
  return universities