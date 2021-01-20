import psycopg2 as dbapi2

dsn = "postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


def getAllRestaurants():
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select restaurant.id as id, restaurant.name as name, category.name as catname" \
                    " from restaurant left join category on (restaurant.categoryid = category.id) order by restaurant.name"
            cursor.execute(query)
            for id, name, catname in cursor:
                element = []
                element.append(id)
                element.append(name)
                element.append(catname)
                restaurants.append(element)
    return restaurants


def getAllRestaurantsWithUniversity(universityId):
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select restaurant.id as id, restaurant.name as name, category.name as catname," \
                    " restaurant.menupdf as menupdf from restaurant left join category on (restaurant.categoryid = category.id)" \
                    " left outer join service s on restaurant.id = s.restaurantid" \
                    " where(s.universityid=%s) order by restaurant.name"
            cursor.execute(query, (universityId,))
            for id, name, catname, menupdf in cursor:
                element = []
                element.append(id)
                element.append(name)
                element.append(catname)
                element.append(menupdf)
                restaurants.append(element)
    return restaurants


def getRestaurant(restaurantId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select *, restaurant.name as restaurantname from restaurant left join category on (restaurant.categoryid = category.id) where(restaurant.id = %s) "
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                restaurant = dict(zip(columns, cursor.fetchone()))
            return restaurant


def getMostPopularRestaurants():
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select m.restaurantid, Count(m.restaurantid),r.name from ordercontent left join menu m on" \
                    " ordercontent.menuid = m.id left outer join restaurant r on r.id = m.restaurantid group by " \
                    "m.restaurantid, r.name order by count desc limit 5"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    restaurants.append(dict(zip(columns, i)))
                return restaurants
    return restaurants


def getMostPopularMenusByRestaurantId(restaurantId):
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select m.name as menuname, Count(m.name),r.name from ordercontent left join menu m on" \
                    " ordercontent.menuid = m.id left outer join restaurant r on r.id = m.restaurantid " \
                    "where (m.restaurantid=%s) group by " \
                    "m.name, r.name order by count desc limit 5"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    restaurants.append(dict(zip(columns, i)))
                return restaurants
    return restaurants


def getMostPopularMenusByStudentId(studentId):
    menus = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select m.name as menuname, Count(m.name),r.name from ordercontent left join menu m on" \
                    " ordercontent.menuid = m.id left outer join restaurant r on r.id = m.restaurantid " \
                    "left join orderstudentmatching o on ordercontent.id = o.ordercontentid where(o.studentid=%s) " \
                    "group by " \
                    "m.name, r.name order by count desc limit 5"
            cursor.execute(query, (studentId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    menus.append(dict(zip(columns, i)))
                return menus
    return menus


def getMostPopularRestaurantsByStudentId(studentId):
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select m.restaurantid, Count(m.restaurantid),r.name as restaurantname from ordercontent left join menu m on" \
                    " ordercontent.menuid = m.id left outer join restaurant r on r.id = m.restaurantid " \
                    "left join orderstudentmatching o on ordercontent.id = o.ordercontentid " \
                    "where(o.studentid=%s) group by " \
                    "m.restaurantid, r.name order by count desc limit 5"
            cursor.execute(query, (studentId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    restaurants.append(dict(zip(columns, i)))
                return restaurants
    return restaurants


def getMostPopularCampaigns():
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select m.name as menuname, Count(m.id),r.name as restaurantname from ordercontent left join " \
                    "menu m on ordercontent.menuid = m.id " \
                    "left outer join restaurant r on r.id = m.restaurantid where(m.iscampaign=TRUE )group by " \
                    "m.name, r.name order by count desc limit 10"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    campaigns.append(dict(zip(columns, i)))
                return campaigns
    return campaigns


def getMostOrderingStudents():
    students = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select student.username, count(student.id) from student left join orderstudentmatching o on " \
                    "o.studentid=student.id group by student.username" \
                    " order by count desc limit 10"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    students.append(dict(zip(columns, i)))
                return students
    return students


def getNumberofDeliveredOrders():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select count(ordercontent) as ordercount " \
                    "from ordercontent where (isdelivered=TRUE)"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            ordercount = dict(zip(columns, cursor.fetchone()))
            return ordercount


def getAverageDeliverTime():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select AVG(ordercontent.deliverytime - ordercontent.ordertime) as averagetime " \
                    "from ordercontent where (isdelivered=TRUE)"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            time = dict(zip(columns, cursor.fetchone()))
            return time


def filterRestaurant(name, categoryId, universityId):
    restaurant = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            if name != "" and categoryId != '0':
                name = '%' + name + '%'
                query = "select restaurant.id as id, restaurant.name as name, category.name as catname " \
                        "from restaurant left join category on (restaurant.categoryid = category.id) " \
                        "left  join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND restaurant.categoryid = %s AND LOWER(restaurant.name ) like LOWER(%s)) order by restaurant.name "
                cursor.execute(query, (universityId, categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select restaurant.id as id, restaurant.name as name, category.name as catname " \
                        " from restaurant join category on (restaurant.categoryid = category.id) " \
                        "left  join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND " \
                        "LOWER(restaurant.name ) like LOWER(%s)) order by restaurant.name "
                cursor.execute(query, (universityId, name))
            elif categoryId != '0':
                query = "select restaurant.id as id, restaurant.name as name, category.name as catname " \
                        "from restaurant join category on (restaurant.categoryid = category.id) " \
                        "left  join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND " \
                        "restaurant.categoryid = %s) order by restaurant.name "
                cursor.execute(query, (universityId, categoryId))
            else:
                query = "select restaurant.id as id, restaurant.name as name, category.name as catname" \
                        " from restaurant join category on (restaurant.categoryid = category.id) " \
                        "left  join service s on restaurant.id = s.restaurantid where(s.universityid=%s) order by restaurant.name"
                cursor.execute(query, (universityId,))
            for id, name, catname in cursor:
                element = []
                element.append(id)
                element.append(name)
                element.append(catname)
                restaurant.append(element)
    return restaurant


def deleteRestaurantById(restaurantId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from restaurant where (id=%s)"
                cursor.execute(query, (restaurantId,))
                return True
    except:
        return False


def getAllRestaurantsByCategoryId(catId):
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select name, email from restaurant where (categoryid = %s)"
            cursor.execute(query, (catId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    restaurants.append(dict(zip(columns, i)))
                return restaurants
            else:
                return None


def getRestaurantById(restaurantId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select *, restaurant.name as restaurantname, restaurant.id as restaurantId from restaurant left join category on (restaurant.categoryid = category.id) where (restaurant.id = %s) "
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            restaurant = dict(zip(columns, cursor.fetchone()))
            if restaurant:
                return restaurant
            else:
                return None


def editRestaurantById(restaurantId, name, categoryid, phone):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                if categoryid != '0':
                    query = "update restaurant set name=%s, categoryid=%s, phonenumber=%s where (id=%s)"
                    cursor.execute(query, (name, categoryid, phone, restaurantId))
                else:
                    query = "update restaurant set name=%s, phonenumber=%s, categoryid=NULL where (id=%s)"
                    cursor.execute(query, (name, phone, restaurantId))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail


def getAllRestaurantsForm():
    restaurants = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from restaurant"
            cursor.execute(query)
            for i in cursor:
                restaurants.append((i[0], i[1]))
    return restaurants


def insertPdfToRestaurant(restaurantId, menupdf):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "update restaurant set menupdf=%s where (id=%s)"
            cursor.execute(query, (menupdf, restaurantId))
            return True


def deletePdfFromRestaurant(restaurantId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "update restaurant set menupdf=%s where (id=%s)"
            cursor.execute(query, ('', restaurantId))
            return True


def isServesToStudent(studentId, restaurantId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select universityid as id from student where (student.id=%s)" \
                    " INTERSECT " \
                    "select  universityid as id from service where (service.restaurantid=%s)"
            cursor.execute(query, (studentId, restaurantId))
            if cursor.rowcount > 0:
                return True
            return False


def studentOrderCountFromMenu(studentId, menuId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select count(*) from (select orderstudentmatching.id as id" \
                        "  from student left join orderstudentmatching on (orderstudentmatching.studentid = student.id) " \
                        " where (student.id=%s) INTERSECT select orderstudentmatching.id as id  from ordercontent left join" \
                        " orderstudentmatching on (orderstudentmatching.ordercontentid = ordercontent.id)  where" \
                        " (ordercontent.menuid=%s) )I"
                cursor.execute(query, (studentId, menuId))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    return dict(zip(columns, cursor.fetchone()))['count']
                return False
    except:
        return False
