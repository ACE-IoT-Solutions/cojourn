from flask import Flask, Blueprint
from flask.helpers import url_for
from apis import api_blueprint
import logging
from flask_jwt_extended import JWTManager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super secret"
    app.register_blueprint(api_blueprint)
    jwt = JWTManager(app)
    
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.debug("Starting api at 127.0.0.1:5000/api/v1")
    
    app.run(debug=True)
    