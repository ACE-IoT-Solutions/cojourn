from http import HTTPStatus
from api_mock.apis.dao.device_dao import DeviceDAO

from api_mock.apis.dao.hems_dao import HEMSDAO
from api_mock.apis.model.hems import hems, hems_der_status
from api_mock.apis.namespace import hems_ns
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from state import load_state, save_state


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
            state["devices"] = DAO.set_all_der_status(status)
            save_state(state)

            return DAO.get(), HTTPStatus.OK