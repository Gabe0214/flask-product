from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models.models import db as main_db, ma
from registration.registration import register
from products.route import product_route
from admin.admin import admin_route

# Init App

app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config.from_object('settings.DevelopmentConfig')
else:
    app.config.from_object('settings.ProductionConfig')
main_db.init_app(app)
ma.init_app(app)


with app.app_context():
    app.register_blueprint(register)
    app.register_blueprint(product_route)
    app.register_blueprint(admin_route)


CORS(app)
bcrypt = Bcrypt(app)

# run server
if __name__ == '__main__':
    app.run()
