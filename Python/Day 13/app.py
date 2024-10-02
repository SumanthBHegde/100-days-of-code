from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import config
from routes import auth_blueprint, product_blueprint, order_blueprint
from models import db, TokenBlocklist

app = Flask(__name__)
app.config.from_object(config['development'])
migrate = Migrate(app, db)

db.init_app(app)
jwt = JWTManager(app)

# Token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

# Handle expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {
        "msg": "The token has expired",
        "error": "token_expired"
    }, 401

# Register routes
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(product_blueprint, url_prefix="/products")
app.register_blueprint(order_blueprint, url_prefix="/orders")

if __name__ == '__main__':
    app.run(debug=True)