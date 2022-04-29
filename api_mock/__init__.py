from flask import Flask, Blueprint, redirect
from flask.helpers import url_for
from api_mock.apis import api_blueprint
from api_mock.apis.dao.auth_dao import AuthDAO
from api_mock.apis.protocols import AuthProtocol
from api_mock.extensions import jwt
from dotenv import load_dotenv
from werkzeug.utils import import_string
from config import Config


def create_app(config: str, auth_dao: AuthProtocol=None) -> Flask:
    app = Flask(__name__)
    cfg = import_string(f"config.{config}")  
    app.config.from_object(cfg)
    app.config["JWT_SECRET_KEY"] = "super secret"
    app.register_blueprint(api_blueprint)
    jwt.init_app(app)
   
    @app.route("/")
    @app.route('/<path:path>')
    def default_route(path=None):
        return redirect(url_for("api.doc"))
    
    return app
