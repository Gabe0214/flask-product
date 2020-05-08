from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_jwt import JWT, jwt_required, current_identity
from flask_migrate import Migrate
# Init App
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Init ma
ma = Marshmallow(app)

# Product class/model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# product schema 
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    user_email = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(10))
    admin = db.Column(db.Boolean)

    def __init__(self, user_name, user_email, user_password, admin):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.admin = admin

# user Schema
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'user_email', 'user_password')


# Init schema


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
# create a product


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
# get all products


@app.route('/product', methods =['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# GET a single product
@app.route('/product/<id>', methods =['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)



# Update a product


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "product does not exist"})
    else:
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']

        product.name = name
        product.description = description
        product.price = price
        product.qty = qty

        db.session.commit()
        return product_schema.jsonify(product)
# Delete a product


@app.route('/product/<id>', methods=['DELETE'])
def del_product(id):
    product = Product.query.get(id)
    if not id:
        return jsonify({"msg": "id does not exist"})
    else:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"msg": "product deleted"})

#Authentication is needed.
@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'pasword':
        return jsonify({"msg": "You're in"})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})

# run server

if __name__ == '__main__':
    app.run(debug=True)
