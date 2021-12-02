from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restx import fields, Namespace, Resource


api = Namespace('hems', description='HEMS Operations')
hems = api.model('HEMS', {
    'id': fields.String(readonly=True, description='The HEMS unique identifier'),
    'provisioned': fields.Boolean(required=True, description='The HEMS\'s Provisioned Status'),
})

class HEMSDAO(object):
    def __init__(self):
        self.tokens = []



@api.route('/')
class HEMS(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.doc('list_hems')
    @api.marshal_list_with(hems)
    @jwt_required()
    def get(self):
        '''List all tasks'''


    @api.doc('create_todo')
    @api.expect(hems)
    @api.marshal_with(hems, code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new task'''
        pass