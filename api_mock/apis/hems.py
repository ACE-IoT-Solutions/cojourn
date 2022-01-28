from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restx import fields, Namespace, Resource

from .device import DAO as device_DAO

from .types import DemandResponseStatus
from state import load_state, save_state


hems_ns = Namespace('hems', description='HEMS Operations')
hems = hems_ns.model('HEMS', {
    'id': fields.String(readonly=True, description='The HEMS unique identifier'),
    'provisioned': fields.Boolean(required=True, description='The HEMS\'s Provisioned Status'),
})

hems_der_status = hems_ns.model('HemsDerStatus', {"status": fields.String(required=True, enum=[status for status in DemandResponseStatus], description='The HEMS\'s Der Status')})

class HEMSDAO(object):
    def __init__(self, home=None):
        self.home = home
        self.tokens = []
       
    def get(self):
        if self.home is None:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"home doesn't exist")    
        return self.home
    
    def get_id(self, id):
        if self.home["id"] != id:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"home with id {id} doesn't exist")
        return self.home

    def create(self, data):
        self.home = data
        return self.home

    def update(self, data):
        self.home.update(data)
        return self.home

    def set_der_status(self, id, status):
        if self.home["id"] != id:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"home with id {id} doesn't exist")
        return device_DAO.set_all_der_status(status)
        

    def delete(self):
        self.home = None

    

state = load_state()
DAO = HEMSDAO(state.get("home", None))

@hems_ns.route('/')
class HEMS(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @hems_ns.doc('list_hems')
    @hems_ns.marshal_list_with(hems)
    @jwt_required()
    def get(self):
        '''List all tasks'''
        return DAO.get(), HTTPStatus.OK

@hems_ns.route('/<string:id>/set_der_status')
class HEMSDERStatus(Resource):
    @hems_ns.doc('set_der_status')
    @hems_ns.expect(hems_der_status)
    @hems_ns.marshal_with(hems)
    @jwt_required()
    def post(self, id):
        '''Set the HEMS\'s Der Status'''
        if id == DAO.get()["id"]:
            devices = DAO.set_der_status(id, hems_ns.payload["status"])
            state["devices"] = devices
            save_state(state)
            return DAO.get(), HTTPStatus.OK


