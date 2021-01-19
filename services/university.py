import psycopg2 as dbapi2

dsn = "postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


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
