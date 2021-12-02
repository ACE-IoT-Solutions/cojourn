from flask_restx import fields, Namespace, Resource


api = Namespace('users', description='User Operations')
user = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='The User\'s First Name'),
    'last_name': fields.String(required=True, description='The User\'s Last Name'),
    'birthdate': fields.Date(required=True, description='The User\'s Birthdate'),
    'email': fields.String(required=True, description='The User\'s Email'),
})


class UserDAO(object):
    pass
    
    
@api.route("/")
class UserList(Resource):
    pass

