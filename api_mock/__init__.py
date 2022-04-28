from flask import Flask, Blueprint, redirect
from flask.helpers import url_for
from api_mock.apis import api_blueprint
from flask_jwt_extended import JWTManager

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super secret"
    app.register_blueprint(api_blueprint)
    jwt = JWTManager(app)
   
    @app.route("/")
    @app.route('/<path:path>')
    def default_route(path=None):
        return redirect(url_for("api.doc"))
    
    return app
