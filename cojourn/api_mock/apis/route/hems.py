from http import HTTPStatus
from cojourn.api_mock.apis.dao import DeviceDAO

from cojourn.api_mock.apis.dao import HEMSDAO
from cojourn.api_mock.apis.model.hems import hems, hems_der_status, hems_jwt
from cojourn.api_mock.apis.namespace import hems_ns
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from cojourn.state import load_state, save_state
from flask import current_app
import os

state = load_state()
JWT_FILE = "/var/lib/volttron/cojourn.jwt"

@hems_ns.route('/')
class HEMS(Resource):
    @hems_ns.doc('get_hems')
    @hems_ns.marshal_list_with(hems)
    @jwt_required()
    def get(self):
        '''Get HEMS Config'''
        return current_app.config["HEMSDAO"].get(), HTTPStatus.OK

@hems_ns.route('/<string:id>/set_der_status')
class HEMSDERStatus(Resource):
    @hems_ns.doc('set_der_status')
    @hems_ns.expect(hems_der_status)
    @hems_ns.marshal_with(hems)
    @jwt_required()
    def post(self, id):
        '''Set the HEMS\'s Der Status'''
        hems = current_app.config["HEMSDAO"].get()
        if id == hems["id"]:
            status = hems_ns.payload["status"]
            hems["dr_status"] = status
            state["hems"] = hems
            state["devices"] = current_app.config["HEMSDAO"].set_der_status(id, status)
            save_state(state)

            return current_app.config["HEMSDAO"].get(), HTTPStatus.OK

@hems_ns.route('/generate_new_jwt')
class HEMSJWTGen(Resource):
    @hems_ns.doc('generate_new_jwt')
    @hems_ns.marshal_with(hems_jwt)
    def post(self):
        '''Generate a new JWT'''

        if not state.get('jwt'):
            current_app.jwt = current_app.config["HEMSDAO"].generate_new_jwt()
            state['jwt'] = True
            save_state(state)
            return current_app.config["HEMSDAO"].get(), HTTPStatus.OK