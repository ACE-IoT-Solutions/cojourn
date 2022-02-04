from flask_restx import fields, Namespace, Resource
from api_mock.apis.namespace import user_ns


    
@user_ns.route("/")
class UserList(Resource):
    pass
