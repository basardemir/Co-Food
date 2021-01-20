import psycopg2 as dbapi2

dsn = "postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"


def getAllCampaigns():
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId," \
                    " restaurant.name as restaurantName from menu join restaurant on (restaurant.id = menu.restaurantid) where(menu.iscampaign = true)" \
                    "order by menu.name"
            cursor.execute(query)
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    campaigns.append(dict(zip(columns, i)))
                return campaigns
            else:
                return None


def getAllCampaignsWithUniversity(restaurantId):
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId," \
                    " restaurant.name as restaurantName from menu inner join restaurant on (restaurant.id = menu.restaurantid) " \
                    " inner join service s on restaurant.id = s.restaurantid" \
                    " where(menu.iscampaign = true AND s.universityid=%s )" \
                    "order by menu.name"
            cursor.execute(query, (restaurantId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    campaigns.append(dict(zip(columns, i)))
                return campaigns
            else:
                return None


def filterCampaign(name, categoryId, universityId):
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            if name != "" and categoryId != '0':
                name = '%' + name + '%'
                query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId," \
                        " restaurant.name as restaurantName from menu left join restaurant on (restaurant.id = menu.restaurantid) " \
                        " left outer join service s on restaurant.id = s.restaurantid " \
                        "where(s.universityid=%s AND menu.iscampaign = true AND restaurant.categoryid = %s AND LOWER(menu.name ) like LOWER(%s)) " \
                        "order by menu.name"
                cursor.execute(query, (universityId, categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId," \
                        " restaurant.name as restaurantName from menu left join restaurant on (menu.restaurantid = restaurant.id ) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND  " \
                        "menu.iscampaign = true AND LOWER(menu.name ) like LOWER(%s)) order by menu.name "
                cursor.execute(query, (universityId, name))
            elif categoryId != '0':
                query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId," \
                        " restaurant.name as restaurantName from menu left join restaurant on (restaurant.categoryid = restaurant.id ) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND  " \
                        "menu.iscampaign = true AND restaurant.categoryid = %s)  order by menu.name"
                cursor.execute(query, (universityId, categoryId))
            else:
                query = "select price, menu.name as name, menu.description as content, s.restaurantid as restaurantId, " \
                        "restaurant.name as restaurantName" \
                        " from menu left join restaurant on (restaurant.id = menu.restaurantid) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND menu.iscampaign = true)" \
                        " order by menu.name"
                cursor.execute(query, (universityId,))
            columns = list(cursor.description[i][0] for i in range(0, len(cursor.description)))
            if cursor.rowcount > 0:
                for i in cursor:
                    campaigns.append(dict(zip(columns, i)))
                return campaigns
            else:
                return None
