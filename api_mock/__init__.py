from flask import Flask, Blueprint
from flask.helpers import url_for
from .apis import api_blueprint
from flask_jwt_extended import JWTManager

def create_app() -> Flask:
    print("creating app")
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super secret"
    app.register_blueprint(api_blueprint)
    jwt = JWTManager(app)
    
    return app
