from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
# Init App
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bcrypt = Bcrypt(app)

# config env variable setup

app.config.from_envvar('APP_SETTINGS')


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
    user_password = db.Column(db.String(10))
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
# create a product

# token middle-ware

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "token is missing"})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(user_name=data['user_name']).first()
        except:
                return jsonify({"message":"token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

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
        image_url = request.json['image_url']
        
        product.name = name
        product.description = description
        product.price = price
        product.qty = qty
        product.image_url = image_url
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
@app.route('/register', methods=['POST'])
def user_register():
# verify that user exist by checking the email, and username || implement some sort of middleware
# hash the password, so that it is not fully exposed
    
    user_name = request.json['user_name']
    user_email = request.json['user_email']
    user_password = request.json['user_password']
    admin = False
    pw_hash = bcrypt.generate_password_hash(user_password)

    new_user = Users(user_name, user_email, pw_hash, admin)

    db.session.add(new_user)
    db.session.commit() 
    return user_schema.jsonify(new_user)


# grant admin permission to user
@app.route('/admin/<user_id>', methods=['PUT'])
def admin_verify(user_id):
    user = Users.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User does not exist"})
    else:
        user.admin = True
        db.session.commit()
        return user_schema.jsonify(user)

    


## token i given upon login success
@app.route('/login', methods=['POST'])
def login():
   user_name = request.json['user_name']
   password = request.json['password']

   if not user_name or not password:
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})
   user = Users.query.filter_by(user_name= user_name).first()
 
 
   if not user:
        return jsonify({"message": "user does not exist"})
    
   if bcrypt.check_password_hash(user.user_password, password):
        token = jwt.encode({'user_name': user.user_name, 'admin': user.admin, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})
   return jsonify({"message": "invalid credentials"})
        

## route for all users, if the user is an admin

@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "You don not have admin privileges to access this route"})
   
    users = Users.query.all()
    result = users_schema.dump(users)
    return jsonify(result)


# run server

if __name__ == '__main__':
    app.run()
 