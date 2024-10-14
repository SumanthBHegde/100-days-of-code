from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from routes.auth_routes import auth_bp
from routes.project_routes import project_bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
jwt = JWTManager(app)

#Swagger UI setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Project API"})
app.register_blueprint(swaggerui_blueprint)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(project_bp, url_prefix='/projects')

if __name__ == '__main__':
    app.run(debug=True)