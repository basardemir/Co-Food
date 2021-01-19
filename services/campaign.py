import psycopg2 as dbapi2


dsn="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"

def getAllCampaigns():
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from menu join restaurant on (restaurant.id = menu.restaurantid) where(menu.iscampaign = true)" \
                    "order by menu.name"
            cursor.execute(query)
            for i in cursor:
                element_dic = {
                    "price": i[1],
                    "name": i[2],
                    "content": i[3],
                    "restaurantId": i[5],
                    "restaurantName": i[7],
                }
                campaigns.append(element_dic)
    return campaigns

def getAllCampaignsWithUniversity(restaurantId):
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            query = "select * from menu inner join restaurant on (restaurant.id = menu.restaurantid) " \
                    " inner join service s on restaurant.id = s.restaurantid" \
                    " where(menu.iscampaign = true AND s.universityid=%s )" \
                    "order by menu.name"
            cursor.execute(query,(restaurantId,))
            for i in cursor:
                element_dic = {
                    "price": i[1],
                    "name": i[2],
                    "content": i[3],
                    "restaurantId": i[5],
                    "restaurantName": i[7],
                }
                campaigns.append(element_dic)
    return campaigns


def filterCampaign(name, categoryId,universityId):
    campaigns = []
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            if name != "" and categoryId != '0':
                name = '%' + name + '%'
                query = "select * from menu left join restaurant on (restaurant.id = menu.restaurantid) " \
                        " left outer join service s on restaurant.id = s.restaurantid " \
                        "where(s.universityid=%s AND menu.iscampaign = true AND restaurant.categoryid = %s AND LOWER(menu.name ) like LOWER(%s)) " \
                        "order by menu.name"
                cursor.execute(query, (universityId,categoryId, name))
            elif name != "":
                name = '%' + name + '%'
                query = "select * from menu left join restaurant on (menu.restaurantid = restaurant.id ) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND  " \
                        "menu.iscampaign = true AND LOWER(menu.name ) like LOWER(%s)) order by menu.name "
                cursor.execute(query, (universityId,name))
            elif categoryId != '0':
                query = "select * from menu left join restaurant on (restaurant.categoryid = restaurant.id ) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND  " \
                        "menu.iscampaign = true AND restaurant.categoryid = %s)  order by menu.name"
                cursor.execute(query, (universityId,categoryId))
            else:
                query = "select * from menu left join restaurant on (restaurant.id = menu.restaurantid) " \
                        "left outer join service s on restaurant.id = s.restaurantid where(s.universityid=%s AND menu.iscampaign = true)" \
                        " order by menu.name"
                cursor.execute(query,(universityId,))
            for i in cursor:
                element_dic = {
                    "price": i[1],
                    "name": i[2],
                    "content": i[3],
                    "restaurantId": i[5],
                    "restaurantName": i[7],
                }
                campaigns.append(element_dic)
    return campaigns
