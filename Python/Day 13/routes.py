from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)
from models import db, User, Product, Order, TokenBlocklist

auth_blueprint = Blueprint("auth", __name__)
product_blueprint = Blueprint("products", __name__)
order_blueprint = Blueprint("orders", __name__)

# Authentication Routes
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@auth_blueprint.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    return jsonify({"msg": "Token revoked"}), 200

# Product Routes
@product_blueprint.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock
    } for product in products]), 200

@product_blueprint.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock
    }), 200

# Order Routes
@order_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    product = Product.query.get(product_id)
    if not product or product.stock < quantity:
        return jsonify({"msg": "Product not available or insufficient stock"}), 400

    total_price = product.price * quantity
    order = Order(user_id=get_jwt_identity(), product_id=product.id, quantity=quantity, total_price=total_price)

    product.stock -= quantity
    db.session.add(order)
    db.session.commit()

    return jsonify({"msg": "Order placed successfully", "order_id": order.id}), 201
