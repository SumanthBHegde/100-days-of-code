from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["JWT_SECRET_KEY"] = "456#sup@SIR" 

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Blocklist for revoked tokens
BLOCKLIST = set()

# Check if the token is revoked
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token': access_token}), 200

# Profile route
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_data = User.query.filter_by(username=current_user).first()

    if user_data is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'username': user_data.username
    }), 200

# Logout route
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Get the unique identifier for the JWT
    jti = get_jwt()['jti'] 
    
    # Add the token to the blocklist 
    BLOCKLIST.add(jti)      
    return jsonify({"msg": "Successfully logged out"}), 200

if __name__ == '__main__':
    app.run(debug=True)
