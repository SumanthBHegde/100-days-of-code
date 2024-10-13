from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, Product

order_blueprint = Blueprint('orders', __name__)

# Create Order Route
@order_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    user_id = get_jwt_identity()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Product not found'}), 404

    order = Order(product_id=product_id, user_id=user_id, quantity=quantity)
    db.session.add(order)
    db.session.commit()

    return jsonify({'msg': 'Order placed'}), 201
