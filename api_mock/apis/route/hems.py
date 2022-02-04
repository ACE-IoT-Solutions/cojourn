from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restx import fields, Namespace, Resource

from api_mock.apis.dao.hems_dao import HEMSDAO
from api_mock.apis.model.hems import hems, hems_der_status

from .device import DAO as device_DAO

from api_mock.apis.types import DemandResponseStatus
from state import load_state, save_state
from api_mock.apis.namespace import hems_ns




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
