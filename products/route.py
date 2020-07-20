from flask import Blueprint, jsonify, request
from models.models import Product, products_schema, db, product_schema

product_route = Blueprint('product_route', __name__)


@product_route.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get a single product
@product_route.route('/product/<id>', methods =['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Delete a product
@product_route.route('/product/<id>', methods=['DELETE'])
def del_product(id):
    product = Product.query.get(id)
    if not id:
        return jsonify({"msg": "id does not exist"})
    else:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"msg": "product deleted"})


# Add a product
@product_route.route('/product', methods=['POST'])
def add_product():

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    image_url = request.json['image_url']
    new_product = Product(name, description, price, qty, image_url)
    if Product.query.filter_by(name= name).first():
        return jsonify({"msg": "product already exist"})
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@product_route.route('/product/<id>', methods=['PUT'])
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
