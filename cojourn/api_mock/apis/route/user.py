from cojourn.api_mock.apis.namespace import user_ns
from flask_restx import Resource


@user_ns.route("/")
class UserList(Resource):
    pass
