import psycopg2 as dbapi2

dsn = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""
dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


def hasActiveOrder(studentId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from orderstudentmatching left join ordercontent o on " \
                    "o.id = orderstudentmatching.ordercontentid where (studentid=%s AND o.isDelivered = FALSE)"
            cursor.execute(query, (studentId,))
            if cursor.fetchone():
                return True
            else:
                return False


def insertOrderSQL(menuId, studentId, numberofstudents, menucount, address):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                # query = """BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED;insert into ordercontent
                # (ordertime, menuid,numberofstudents,menucount,address) values (CURRENT_DATE,%s,%s,%s,%s)
                # RETURNING id as ID;insert into orderstudentmatching (studentid,ordercontentid) values (%s,ID);
                # COMMIT;"""
                query = "insert into ordercontent (ordertime, menuid,numberofstudents,menucount,address) values (CURRENT_TIMESTAMP,%s,%s,%s,%s) RETURNING id"
                cursor.execute(query, (menuId, numberofstudents, menucount, address))
                id = cursor.fetchone()
                query = "insert into orderstudentmatching (studentid,ordercontentid) values (%s,%s)"
                cursor.execute(query, (studentId, id))
                return True
    except:
        return False


def getOrderDetails(studentId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontentid as id,ordertime, m.name as menuname,r.name as restaurantname," \
                        " m.description as description, menucount, address,price,numberofstudents" \
                        " from orderstudentmatching left join ordercontent o on " \
                        "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                        "left join restaurant r on r.id = m.restaurantid where (studentid=%s AND o.isDelivered = FALSE)"
                cursor.execute(query, (studentId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    order = dict(zip(columns, cursor.fetchone()))
                    return order
                else:
                    return None
    except:
        return False

def getOrderDetailsByOrderId(orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontentid as id, r.id as restaurantid, ordertime, m.name as menuname,r.name as restaurantname," \
                        " m.description as description, menucount, address,price,numberofstudents" \
                        " from orderstudentmatching left join ordercontent o on " \
                        "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                        "left join restaurant r on r.id = m.restaurantid where (orderstudentmatching.ordercontentid=%s )"
                cursor.execute(query, (orderId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    order = dict(zip(columns, cursor.fetchone()))
                    return order
                else:
                    return None
    except:
        return False


def getPastOrders(studentId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontentid as id,ordertime, o.isdelivered, m.name as menuname,r.name as restaurantname," \
                        " m.description as description, menucount, address,price,numberofstudents" \
                        " from orderstudentmatching left join student s on orderstudentmatching.studentid = s.id left join ordercontent o on " \
                        "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                        "left join restaurant r on r.id = m.restaurantid where (studentid=%s AND o.isDelivered = TRUE)" \
                        " GROUP BY ordercontentid"
                cursor.execute(query, (studentId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    order = dict(zip(columns, cursor.fetchone()))
                    return order
                else:
                    return None
    except:
        return False


def getAllPastOrders():
    orders = []
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontent.id as id,ordertime, ordercontent.isdelivered, " \
                        "m.name as menuname,r.name as restaurantname, m.description as description," \
                        " menucount, address,price,numberofstudents FROM ordercontent left join menu" \
                        " m on m.id = ordercontent.menuid left join restaurant r on r.id = m.restaurantid" \
                        " order by ordercontent.ordertime desc  "
                cursor.execute(query)
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    for i in cursor:
                        orders.append(dict(zip(columns, i)))
                    return orders
                else:
                    return None
    except:
        return False

def getAllPastOrdersWithRestaurantId(restaurantId):
    orders = []
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontent.id as id,ordertime, ordercontent.isdelivered, " \
                        "m.name as menuname,  r.name as restaurantname, r.id as restaurantid, m.description as description," \
                        " menucount, address,price,numberofstudents FROM ordercontent left join menu" \
                        " m on m.id = ordercontent.menuid left join restaurant r on r.id = m.restaurantid" \
                        " where (restaurantid =%s) order by ordercontent.ordertime desc "
                cursor.execute(query, (restaurantId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    for i in cursor:
                        orders.append(dict(zip(columns, i)))
                    return orders
                else:
                    return None
    except:
        return False

def getOrdersByOrderId(orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontentid as id,ordertime, m.id as menuid, o.isdelivered, m.name as menuname,r.name as restaurantname," \
                        " m.description as description, menucount, address,price,numberofstudents" \
                        " from orderstudentmatching left join student s on orderstudentmatching.studentid = s.id left join ordercontent o on " \
                        "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                        "left join restaurant r on r.id = m.restaurantid where (ordercontentid=%s)"
                cursor.execute(query, (orderId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    order = dict(zip(columns, cursor.fetchone()))
                    return order
                else:
                    return None
    except:
        return False


def getOrderFriends(orderContentId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select orderstudentmatching.id as id, s.username from orderstudentmatching left join student s on s.id = orderstudentmatching.studentid " \
                        " where ordercontentid=%s order by orderstudentmatching.id asc "
                cursor.execute(query, (orderContentId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    friends = []
                    for i in cursor:
                        friends.append(dict(zip(columns, i)))
                    return friends
                else:
                    return None
    except:
        return False


def getAllOrders():
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontent.id as id, ordertime, m.name as menuname,r.name as restaurantname," \
                        " m.description as description, menucount,price,numberofstudents" \
                        " from ordercontent  " \
                        " left join menu m on m.id = ordercontent.menuid " \
                        "left join restaurant r on r.id = m.restaurantid where (ordercontent.isDelivered = FALSE)"
                cursor.execute(query)
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    orders = []
                    for i in cursor:
                        orders.append(dict(zip(columns, i)))
                    return orders
                else:
                    return None
    except:
        return False


def getAllOrdersWithFilter(restaurantName, categoryId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                if restaurantName != "" and categoryId != '0':
                    query = "select ordercontentid as id, ordertime, m.name as menuname,r.name as restaurantname," \
                            " m.description as description, menucount,price,numberofstudents" \
                            " from orderstudentmatching left join ordercontent o on " \
                            "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                            "left join restaurant r on r.id = m.restaurantid where (o.isDelivered = FALSE AND r.categoryid = %s " \
                            "AND LOWER(r.name ) like LOWER(%s))"
                    cursor.execute(query, (restaurantName, categoryId))
                elif restaurantName != "":
                    name = '%' + restaurantName + '%'
                    query = "select ordercontentid as id, ordertime, m.name as menuname,r.name as restaurantname," \
                            " m.description as description, menucount,price,numberofstudents" \
                            " from orderstudentmatching left join ordercontent o on " \
                            "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                            "left join restaurant r on r.id = m.restaurantid where (o.isDelivered = FALSE " \
                            "AND LOWER(r.name ) like LOWER(%s))"
                    cursor.execute(query, (name,))
                elif categoryId != '0':
                    query = "select ordercontentid as id, ordertime, m.name as menuname,r.name as restaurantname," \
                            " m.description as description, menucount,price,numberofstudents" \
                            " from orderstudentmatching left join ordercontent o on " \
                            "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                            "left join restaurant r on r.id = m.restaurantid where (o.isDelivered = FALSE AND r.categoryid = %s " \
                            ")"
                    cursor.execute(query, (categoryId,))
                else:
                    query = "select ordercontentid as id, ordertime, m.name as menuname,r.name as restaurantname," \
                            " m.description as description, menucount,price,numberofstudents" \
                            " from orderstudentmatching left join ordercontent o on " \
                            "o.id = orderstudentmatching.ordercontentid left join menu m on m.id = o.menuid " \
                            "left join restaurant r on r.id = m.restaurantid where (o.isDelivered = FALSE)"
                    cursor.execute(query)
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    orders = []
                    for i in cursor:
                        orders.append(dict(zip(columns, i)))
                    return orders
                else:
                    return None
    except:
        return False


def getActiveOrder(orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "select ordercontentid as id, numberofstudents" \
                        " from orderstudentmatching left join ordercontent o on " \
                        "o.id = orderstudentmatching.ordercontentid " \
                        " where ( o.isDelivered = FALSE AND o.id=%s)"
                cursor.execute(query, (orderId,))
                columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
                if cursor.rowcount > 0:
                    orders = []
                    for i in cursor:
                        orders.append(dict(zip(columns, i)))
                    return orders
                else:
                    return None
    except:
        return False


def insertParticipant(studentId, orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into orderstudentmatching (ordercontentid, studentid) values (%s,%s)"
                cursor.execute(query, (orderId, studentId))
                return True
    except:
        return False


def deleteParticipant(studentId, orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from orderstudentmatching where (ordercontentid =%s and studentid=%s)"
                cursor.execute(query, (orderId, studentId))
                query = "select * from orderstudentmatching where (ordercontentid =%s)"
                cursor.execute(query, (orderId,))
                if cursor.rowcount == 0:
                    query = "delete from ordercontent where (id =%s )"
                    cursor.execute(query, (orderId,))
                return True
    except:
        return False


def sendOrderContent(orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update ordercontent set isdelivered = TRUE, deliverytime=CURRENT_TIMESTAMP where (id=%s)"
                cursor.execute(query, (orderId,))
                return True
    except:
        return False


def deleteOrderById(orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "BEGIN TRANSACTION;" \
                        "delete from ordercontent where (id=%s); " \
                        "delete from orderstudentmatching where (ordercontentid=%s);" \
                        "COMMIT;"
                cursor.execute(query, (orderId, orderId))
                return True
    except:
        return False


def editOrderById(orderId, address, menucount, numberofstudents, menuid):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "update ordercontent set address=%s, menucount=%s, numberofstudents=%s, " \
                        "menuid=%s where (id=%s)"
                cursor.execute(query, (address, menucount, numberofstudents, menuid, orderId))
                return True
    except:
        return False

def addOrderById(address, menucount, numberofstudents, menuid):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into  ordercontent (address, menucount, numberofstudents, menuid,ordertime) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP) RETURNING id"
                cursor.execute(query, (address, menucount, numberofstudents, menuid))
                id = cursor.fetchone()[0]
                return id
    except:
        return False

def addMatchingByStudentOrder(studentId, orderId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "insert into orderstudentmatching (ordercontentid, studentid) values (%s,%s)"
                cursor.execute(query, (orderId, studentId))
                return True
    except:
        return False


def deleteMatchById(matchId):
    try:
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = "delete from orderstudentmatching where (id=%s)"
                cursor.execute(query, (matchId,))
                return True
    except:
        return False


def getMatchById(matchId):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from orderstudentmatching where (id=%s)"
            cursor.execute(query, (matchId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                service = dict(zip(columns, cursor.fetchone()))
                return service
            else:
                return None
