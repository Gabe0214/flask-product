from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


# # Init db
# # db = SQLAlchemy(app)
# # migrate = Migrate(app, db)
# # # Init ma

# Product class/model

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    image_url = db.Column(db.String)

    def __init__(self, name, description, price, qty, image_url):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.image_url = image_url


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty', 'image_url')


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    user_email = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(90))
    admin = db.Column(db.Boolean)

    def __init__(self, user_name, user_email, user_password, admin):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.admin = admin

# marshmallow schema shows the desired fields into the json data


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'user_email', 'user_password', 'admin')


# Init schema


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
