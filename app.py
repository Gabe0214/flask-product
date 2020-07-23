from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models.models import db as main_db, ma, migrate
from registration.registration import register
from products.route import product_route
from admin.admin import admin_route

# Init App
app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config.from_object('settings.DevelopmentConfig')
else:
    app.config.from_object('settings.ProductionConfig')


with app.app_context():
    main_db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, main_db)
    app.register_blueprint(register)
    app.register_blueprint(product_route)
    app.register_blueprint(admin_route)

app.app_context().push()

CORS(app)
bcrypt = Bcrypt(app)
# run server
if __name__ == '__main__':
    app.run()
