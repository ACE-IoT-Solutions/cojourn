from api_mock.apis.route.auth import auth_ns
from api_mock.apis.route.device import device_ns
from api_mock.apis.route.hems import hems_ns
from api_mock.apis.route.home import home_ns
from api_mock.apis.route.user import user_ns
from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
api = Api(api_blueprint,
          authorizations=authorizations,
          security="apikey",
          version='0.0.1',
          title='Cojourn API Mock',
          description='API Mock for testing Cojourn'
          )

api.add_namespace(device_ns)
api.add_namespace(hems_ns)
api.add_namespace(home_ns)
api.add_namespace(user_ns)
api.add_namespace(auth_ns)
