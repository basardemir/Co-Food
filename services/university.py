import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""


class University:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def getAllUniversities():
    universities = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from university"
            cursor.execute(query)
            for i in cursor:
                universities.append(University(i[0], i[1]))
    return universities


def getAllUniversitiesForm():
    universities = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from university"
            cursor.execute(query)
            for i in cursor:
                universities.append((i[0], i[1]))
    return universities


def getAllUniversitiesAdminForm():
    universities = []
    universities.append((0, "None"))
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from university"
            cursor.execute(query)
            for i in cursor:
                universities.append((i[0], i[1]))
    return universities


def deleteUniversityById(uniId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from university where (id=%s)"
                cursor.execute(query, (uniId,))
                return True
    except:
        return False


def addUniversityByName(name):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into university (name) VALUES (%s)"
                cursor.execute(query, (name,))
                return True
    except:
        return False


def getUniversityById(uniId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from university where (id=%s)"
            cursor.execute(query, (uniId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                university = dict(zip(columns, cursor.fetchone()))
                return university
            else:
                return None


def editUniversityById(uniId, name):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update university set name=%s where (id=%s)"
                cursor.execute(query, (name, uniId))
                return True
    except:
        return False


def getAllUniversitiesByRestaurantId(restaurantId):
    universities = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select *, service.id as serviceId from service join restaurant r on r.id = service.restaurantid " \
                    "left join university u on u.id = service.universityid where (service.restaurantid=%s)"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    universities.append(dict(zip(columns, i)))
                print(universities)
                return universities
            else:
                return None
