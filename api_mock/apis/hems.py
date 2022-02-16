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
    'dr_status': fields.String(
        required=True, 
        description="Demand Response Status",
        enum=[status for status in DemandResponseStatus]
    )
})

hems_der_status = hems_ns.model('HemsDerStatus', {"status": fields.String(required=True, enum=[status for status in DemandResponseStatus], description='The HEMS\'s Der Status')})

class HEMSDAO(object):
    def __init__(self, hems=None):
        self.hems = hems
        self.tokens = []
       
    def get(self):
        if self.hems is None:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"HEMS doesn't exist")    
        return self.hems
    
    def get_id(self, id):
        if self.hems["id"] != id:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"HEMS with id {id} doesn't exist")
        return self.hems

    def create(self, data):
        self.hems = data
        return self.hems

    def update(self, data):
        self.hems.update(data)
        return self.hems

    def set_der_status(self, id, status):
        if self.hems["id"] != id:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"HEMS with id {id} doesn't exist")
        
        self.hems.dr_status = status
        return device_DAO.set_all_der_status(status)

    def delete(self):
        self.hems = None

state = load_state()
DAO = HEMSDAO(state.get("hems", {}))

@hems_ns.route('/')
class HEMS(Resource):
    @hems_ns.doc('get_hems')
    @hems_ns.marshal_list_with(hems)
    @jwt_required()
    def get(self):
        '''Get HEMS Config'''
        return DAO.get(), HTTPStatus.OK

@hems_ns.route('/<string:id>/set_der_status')
class HEMSDERStatus(Resource):
    @hems_ns.doc('set_der_status')
    @hems_ns.expect(hems_der_status)
    @hems_ns.marshal_with(hems)
    @jwt_required()
    def post(self, id):
        '''Set the HEMS\'s Der Status'''
        hems = DAO.get()
        if id == hems["id"]:
            status = hems_ns.payload["status"]
            hems["dr_status"] = status
            state["hems"] = hems
            state["devices"] = device_DAO.set_all_der_status(status)
            save_state(state)

            return DAO.get(), HTTPStatus.OK


