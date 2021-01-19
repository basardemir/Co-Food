from flask import Flask
from flask_login import LoginManager
from application.campaign import *
from application.categories import *
from application.home import *
from application.menu import *
from application.order import *
from application.registration import *
from application.restaurant import *
from application.universities import *
from application.user import *
from application.wait_room import *

app = Flask(__name__)
app.config.from_object("settings")
app.config['SECRET_KEY'] = 'any secret string'
WTF_CSRF_ENABLED = True
app.config['db'] = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

lm = LoginManager()

lm.init_app(app)
lm.login_view = "/"


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def page_not_found(e):
    return render_template('errorViews/404.html')


def page_no_authorization(e):
    return render_template('errorViews/403.html')


# restaurant
app.add_url_rule('/restaurant/<int:restaurantId>', view_func=restaurant_details, methods=['GET'])
app.add_url_rule('/restaurant/<int:restaurantId>', view_func=add_comment, methods=['POST'])
app.add_url_rule('/admin/comment/delete/<int:commentId>', view_func=deleteComment, methods=['GET'])
app.add_url_rule('/restaurants', view_func=getRestaurants, methods=['GET'])
app.add_url_rule('/restaurants', view_func=filterRestaurants, methods=['POST'])

# campaigns
app.add_url_rule('/campaigns', view_func=getCampaigns, methods=['GET'])
app.add_url_rule('/campaigns', view_func=filterCampaigns, methods=['POST'])

# history
app.add_url_rule('/history', view_func=userHistory, methods=['GET'])
app.add_url_rule('/settings', view_func=userSettings, methods=['GET'])
app.add_url_rule('/settings', view_func=updateUser, methods=['POST'])

# registration
app.add_url_rule('/register', view_func=register, methods=['GET'])
app.add_url_rule('/register', view_func=addClient, methods=['POST'])
app.add_url_rule('/', view_func=login, methods=['GET'])
app.add_url_rule('/', view_func=loginClient, methods=['POST'])
app.add_url_rule('/logout', view_func=logout_page, methods=['GET'])

# order
app.add_url_rule('/order/<int:menuId>', view_func=orderPage, methods=['GET'])
app.add_url_rule('/order/<int:menuId>', view_func=insertNewOrder, methods=['POST'])
app.add_url_rule('/activeorder', view_func=activeOrder, methods=['GET'])
app.add_url_rule('/participate/<int:orderId>', view_func=participate, methods=['GET'])
app.add_url_rule('/participate/delete/<int:orderId>', view_func=deleteParticipation, methods=['GET'])
app.add_url_rule('/participate/send/<int:orderId>', view_func=sendOrder, methods=['GET'])

# main page
app.add_url_rule('/homepage', view_func=homepage, methods=['GET'])
app.add_url_rule('/homepage', view_func=filter_homepage, methods=['POST'])

# owner main page
app.add_url_rule('/ownerhomepage', view_func=ownerhomepage, methods=['GET'])
app.add_url_rule('/owner/restaurant/', view_func=editOwnerRestaurant, methods=['GET'])
app.add_url_rule('/owner/restaurant/', view_func=saveOwnerRestaurant, methods=['POST'])
app.add_url_rule('/owner/service/delete/<int:serviceId>', view_func=deleteOwnerService, methods=['GET'])
app.add_url_rule('/owner/menu/add/', view_func=addOwnerMenu, methods=['GET'])
app.add_url_rule('/owner/menu/add/', view_func=insertOwnerMenu, methods=['POST'])
app.add_url_rule('/owner/menu/edit/<int:menuId>', view_func=editOwnerMenu, methods=['GET'])
app.add_url_rule('/owner/menu/edit/<int:menuId>', view_func=saveOwnerMenu, methods=['POST'])
app.add_url_rule('/owner/menu/delete/<int:menuId>', view_func=deleteOwnerMenu, methods=['GET'])
app.add_url_rule('/owner/orders', view_func=ownerOrders, methods=['GET'])
app.add_url_rule('/owner/order/details/<int:orderId>', view_func=ownerOrderDetails, methods=['GET'])

# admin main page
app.add_url_rule('/adminhomepage', view_func=adminhomepage, methods=['GET'])

# university management
app.add_url_rule('/admin/universities', view_func=adminUniversities, methods=['GET'])
app.add_url_rule('/admin/university/add', view_func=addUniversity, methods=['GET'])
app.add_url_rule('/admin/university/add', view_func=insertUniversity, methods=['POST'])
app.add_url_rule('/admin/university/delete/<int:uniId>', view_func=deleteUniversity, methods=['GET'])
app.add_url_rule('/admin/university/edit/<int:uniId>', view_func=editUniversity, methods=['GET'])
app.add_url_rule('/admin/university/edit/<int:uniId>', view_func=saveUniversity, methods=['POST'])

#order management
app.add_url_rule('/admin/orders', view_func=adminOrders, methods=['GET'])
app.add_url_rule('/admin/order/delete/<int:orderId>', view_func=deleteOrder, methods=['GET'])
app.add_url_rule('/admin/order/edit/<int:orderId>', view_func=editOrder, methods=['GET'])
app.add_url_rule('/admin/order/edit/<int:orderId>', view_func=saveOrder, methods=['POST'])
#app.add_url_rule('/admin/order/edit/<int:orderId>', view_func=saveOrder, methods=['GET'])
app.add_url_rule('/admin/order/add/', view_func=addOrder, methods=['GET'])
app.add_url_rule('/admin/order/add/', view_func=insertOrder, methods=['POST'])


# category management
app.add_url_rule('/admin/categories', view_func=adminCategories, methods=['GET'])
app.add_url_rule('/admin/category/add', view_func=addCategory, methods=['GET'])
app.add_url_rule('/admin/category/add', view_func=insertCategory, methods=['POST'])
app.add_url_rule('/admin/category/delete/<int:catId>', view_func=deleteCategory, methods=['GET'])
app.add_url_rule('/admin/category/edit/<int:catId>', view_func=editCategory, methods=['GET'])
app.add_url_rule('/admin/orderstudentmatching/delete/<int:matchId>', view_func=deleteMatching, methods=['GET'])

# menu management
app.add_url_rule('/admin/menus', view_func=adminMenus, methods=['GET'])

# restaurant management
app.add_url_rule('/admin/restaurants', view_func=adminRestaurants, methods=['GET'])
app.add_url_rule('/admin/restaurant/delete/<int:restaurantId>', view_func=deleteRestaurant, methods=['GET'])
app.add_url_rule('/admin/restaurant/edit/<int:restaurantId>', view_func=editRestaurant, methods=['GET'])
app.add_url_rule('/admin/restaurant/edit/<int:restaurantId>', view_func=saveRestaurant, methods=['POST'])
app.add_url_rule('/admin/service/delete/<int:serviceId>', view_func=deleteService, methods=['GET'])
app.add_url_rule('/admin/menu/delete/<int:menuId>', view_func=deleteMenu, methods=['GET'])
app.add_url_rule('/admin/menu/add/<int:restaurantId>', view_func=addMenuToRestaurant, methods=['GET'])
app.add_url_rule('/admin/menu/add', view_func=addMenu, methods=['GET'])
app.add_url_rule('/admin/menu/add/<int:restaurantId>', view_func=insertMenu, methods=['POST'])
app.add_url_rule('/admin/menu/edit/<int:menuId>', view_func=editMenu, methods=['GET'])
app.add_url_rule('/admin/menu/edit/<int:menuId>', view_func=saveMenu, methods=['POST'])
app.add_url_rule('/admin/menu/pdf/download/<int:restaurantId>', view_func=downloadMenuPdf, methods=['GET'])
app.add_url_rule('/admin/menu/pdf/delete/<int:restaurantId>', view_func=deleteMenuPdf, methods=['GET'])
app.add_url_rule('/owner/menu/pdf/download/<int:restaurantId>', view_func=downloadOwnerMenuPdf, methods=['GET'])
app.add_url_rule('/student/menu/pdf/download/<int:restaurantId>', view_func=downloadStudentMenuPdf, methods=['GET'])
app.add_url_rule('/owner/menu/pdf/delete/<int:restaurantId>', view_func=deleteOwnerMenuPdf, methods=['GET'])

# wait room
app.add_url_rule('/wait-room', view_func=wait_room, methods=['GET'])

# errors
app.register_error_handler(404, page_not_found)
app.register_error_handler(403, page_no_authorization)

if __name__ == '__main__':
    app.run()
