from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restx import fields, Namespace, Resource
from api_mock.apis.namespace import hems_ns
from api_mock.apis.types import DemandResponseStatus


hems = hems_ns.model('HEMS', {
    'id': fields.String(readonly=True, description='The HEMS unique identifier'),
    'provisioned': fields.Boolean(required=True, description='The HEMS\'s Provisioned Status'),
})

hems_der_status = hems_ns.model('HemsDerStatus', {"status": fields.String(required=True, enum=[status for status in DemandResponseStatus], description='The HEMS\'s Der Status')})
