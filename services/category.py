import psycopg2 as dbapi2
from flask import current_app
from passlib.hash import pbkdf2_sha256 as hasher
dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

def getAllCategories():
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      category=[]
      query = "select * from category"
      cursor.execute(query)
      columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
      try:
        if cursor.rowcount > 0:
            for i in cursor:
                cat = dict(zip(columns, i))
                category.append(cat)
            return category
        else:
             return category
      except:
        return None


def getAllCategoriesForm():
  with dbapi2.connect(dsn) as connection:
    with connection.cursor() as cursor:
      category=[]
      category.append((0,"Select Category"))
      query = "select * from category"
      cursor.execute(query)
      try:
        if cursor.rowcount > 0:
            for i in cursor:
                cat = (i[0],i[1])
                category.append(cat)
            return category
        else:
             return category
      except:
        return None