from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_cors import CORS
from models.models import db as main_db, ma
from registration.registration import register
from products.route import product_route
# Init App
import os

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

# basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)
bcrypt = Bcrypt(app)

# config env variable setup


# Init db
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# # Init ma
# ma = Marshmallow(app)
#
# # Product class/model
#
#
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True)
#     description = db.Column(db.String(200))
#     price = db.Column(db.Float)
#     qty = db.Column(db.Integer)
#     image_url = db.Column(db.String)
#     def __init__(self, name, description, price, qty, image_url):
#         self.name = name
#         self.description = description
#         self.price = price
#         self.qty = qty
#         self.image_url = image_url
#
#
# # product schema
# class ProductSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name', 'description', 'price', 'qty', 'image_url')
#
#
# class Users(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(50), unique=True)
#     user_email = db.Column(db.String(100), unique=True)
#     user_password = db.Column(db.String(10))
#     admin = db.Column(db.Boolean)
#
#     def __init__(self, user_name, user_email, user_password, admin):
#         self.user_name = user_name
#         self.user_email = user_email
#         self.user_password = user_password
#         self.admin = admin
#
# # marshmallow schema shows the desired fields into the json data
# class UsersSchema(ma.Schema):
#     class Meta:
#         fields = ('user_id', 'user_name', 'user_email', 'user_password', 'admin')


# Init schema


# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)
# user_schema = UsersSchema()
# users_schema = UsersSchema(many=True)
# create a product

# token middle-ware

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         if not token:
#             return jsonify({"message": "token is missing"})
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = Users.query.filter_by(user_name=data['user_name']).first()
#         except:
#                 return jsonify({"message":"token is invalid"}), 401
#         return f(current_user, *args, **kwargs)
#     return decorated

#
# # grant admin permission to user
# @app.route('/admin/<user_id>', methods=['PUT'])
# def admin_verify(user_id):
#     user = Users.query.get(user_id)
#
#     if not user:
#         return jsonify({"msg": "User does not exist"})
#     else:
#         user.admin = True
#         db.session.commit()
#         return user_schema.jsonify(user)
#
#
#
#

#
#
# ## route for all users, if the user is an admin
#
# @app.route('/users', methods=['GET'])
# @token_required
# def get_all_users(current_user):
#     if not current_user.admin:
#         return jsonify({"message": "You don not have admin privileges to access this route"})
#
#     users = Users.query.all()
#     result = users_schema.dump(users)
#     return jsonify(result)



# run server

if __name__ == '__main__':
    app.run()
