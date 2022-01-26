from flask import Blueprint
from flask_restx import Api

from .device import device_ns as device_ns
from .hems import api as hems_ns
from .user import api as user_ns
from .auth import api as auth_ns
from .home import api as home_ns


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