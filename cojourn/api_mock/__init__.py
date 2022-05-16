from flask import Flask, Blueprint, redirect
from flask.helpers import url_for
from cojourn.api_mock.apis import api_blueprint
from cojourn.api_mock.apis.dao import (
    AuthDAO,
    DeviceDAO,
    HEMSDAO,
    HomeDAO,
    UserDAO
    )
from cojourn.api_mock.apis.protocols import (
    AuthProtocol,
    DeviceProtocol,
    HEMSProtocol,
    HomeProtocol,
    UserProtocol
    )
from cojourn.api_mock.extensions import jwt
from dotenv import load_dotenv
from werkzeug.utils import import_string
from config import Config
from cojourn.state import load_state



def create_app(config: str, auth_dao: AuthProtocol=None, device_dao: DeviceProtocol=None, hems_dao: HEMSProtocol=None, home_dao: HomeProtocol=None, user_dao: UserProtocol=None) -> Flask:
    app = Flask(__name__)
    cfg = import_string(f"config.{config}")  
    app.config.from_object(cfg)
    
    daos = init_daos(
        auth_dao,
        device_dao,
        hems_dao,
        home_dao,
        user_dao
        )
    
    app.config.update(daos)
    
    app.register_blueprint(api_blueprint)
    jwt.init_app(app)
   
    @app.route("/")
    @app.route('/<path:path>')
    def default_route(path=None):
        return redirect(url_for("api.doc"))
    
    return app

def init_daos(auth_dao: AuthProtocol=None, device_dao: DeviceProtocol=None, hems_dao: HEMSProtocol=None, home_dao: HomeProtocol=None, user_dao: UserProtocol=None) -> dict:
    state = load_state()
    
    auth_dao: AuthProtocol = auth_dao if auth_dao else AuthDAO()
    device_dao: DeviceProtocol = device_dao if device_dao else DeviceDAO(state.get("devices", {}))
    hems_dao: HEMSProtocol = hems_dao if hems_dao else HEMSDAO(state.get("hems", {}))
    home_dao: HomeProtocol = home_dao if home_dao else HomeDAO(state.get("home", {}))
    user_dao: UserProtocol = user_dao if user_dao else UserDAO()
    
    return {
        "AuthDAO": auth_dao,
        "DeviceDAO": device_dao,
        "HEMSDAO": hems_dao,
        "HomeDAO": home_dao,
        "UserDAO": user_dao
        }
