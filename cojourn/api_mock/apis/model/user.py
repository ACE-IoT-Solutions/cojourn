from cojourn.api_mock.apis.namespace import user_ns
from flask_restx import fields


user = user_ns.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='The User\'s First Name'),
    'last_name': fields.String(required=True, description='The User\'s Last Name'),
    'birthdate': fields.Date(required=True, description='The User\'s Birthdate'),
    'email': fields.String(required=True, description='The User\'s Email'),
})
