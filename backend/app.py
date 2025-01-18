from flask import Flask
from flask_login import LoginManager

from models import db, Users

from index import index
from login import login
from logout import logout
from register import register
from home import home
from women import women
from men import men
from kids import kids
from header_footer import header_footer
from cart import cart

app = Flask(__name__, static_folder='../frontend/static')

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin_store:123456@localhost/store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Untuk auto-reload template saat pengembangan


login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home) 
app.register_blueprint(women)
app.register_blueprint(men)
app.register_blueprint(kids)
app.register_blueprint(header_footer)
app.register_blueprint(cart)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

