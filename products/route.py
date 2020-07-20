from flask import Blueprint, jsonify, request
from models.models import Product, products_schema

product_route = Blueprint('product_route', __name__)


@product_route.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)
