from application.campaign import *
from application.home import *
from application.order import *
from application.registration import *
from application.restaurant import *
from application.user import *
from application.wait_room import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
WTF_CSRF_ENABLED = True
app.config['db'] = """user=postgres password=basar
host=localhost port=5432 dbname=postgres"""

# restaurant
app.add_url_rule('/restaurant/<int:restaurantId>', view_func=restaurant_details, methods=['GET'])
app.add_url_rule('/restaurants', view_func=getRestaurants, methods=['GET'])

# campaigns
app.add_url_rule('/campaigns', view_func=getCampaigns, methods=['GET'])

# history
app.add_url_rule('/history', view_func=userHistory, methods=['GET'])
app.add_url_rule('/settings', view_func=userSettings, methods=['GET'])

# registration
app.add_url_rule('/register', view_func=register, methods=['GET'])
app.add_url_rule('/register', view_func=add_user, methods=['POST'])
app.add_url_rule('/', view_func=login, methods=['GET'])
app.add_url_rule('/', view_func=loginStudent, methods=['POST'])

# order
app.add_url_rule('/order', view_func=order, methods=['GET'])

# main page
app.add_url_rule('/homepage', view_func=homepage, methods=['GET'])

# wait room
app.add_url_rule('/wait-room', view_func=wait_room, methods=['GET'])

if __name__ == '__main__':
    app.run()