from flask import Blueprint, request, jsonify
from models import db, Product

product_blueprint = Blueprint('products', __name__)

# Add Product Route
@product_blueprint.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    product = Product(name=name, price=price, description=description)
    db.session.add(product)
    db.session.commit()

    return jsonify({'msg': 'Product added'}), 201

# Get All Products Route
@product_blueprint.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    } for product in products]), 200
