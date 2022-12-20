from http import HTTPStatus
from cojourn.api_mock.apis.model.hems import hems, hems_der_status, hems_jwt
from cojourn.api_mock.apis.namespace import hems_ns
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from cojourn.state import load_state, save_state
from flask import current_app
import jwt
import netifaces as ni

state = load_state()
JWT_FILE = "/var/lib/volttron/cojourn.jwt"
SHARED_SECRET = "6a5aa870-ed67-454a-b05d-ba9a5b2d52c5"
MAC_ADDRESS = ni.ifaddresses("eth1")[ni.AF_LINK][0]["addr"].replace(":", "")


@hems_ns.route("/")
class HEMS(Resource):
    """
        Authorized endpoint used to return the current HEMS configuration
    """
    @hems_ns.doc("get_hems")
    @hems_ns.marshal_list_with(hems)
    @jwt_required()
    def get(self):
        """Get HEMS Config"""
        return current_app.config["HEMSDAO"].get(), HTTPStatus.OK


@hems_ns.route("/<string:id>/set_der_status")
class HEMSDERStatus(Resource):
    """
        Authorized endpoint used to set the DER status of a HEMS instance
    """
    @hems_ns.doc("set_der_status")
    @hems_ns.expect(hems_der_status)
    @hems_ns.marshal_with(hems)
    @jwt_required()
    def post(self, id):
        """Set the HEMS\'s Der Status"""
        hems_config = current_app.config["HEMSDAO"].get()
        if id == hems_config["id"]:
            status = hems_ns.payload["status"]
            hems["dr_status"] = status
            state["hems"] = hems
            state["devices"] = current_app.config["HEMSDAO"].set_der_status(id, status)
            save_state(state)

            return current_app.config["HEMSDAO"].get(), HTTPStatus.OK


@hems_ns.route("/generate_new_jwt")
class HEMSJWTGen(Resource):
    """
    Open endpoint used to generate an authorization JWT based
    on a given device's MAC address
    """

    @hems_ns.doc("generate_new_jwt")
    @hems_ns.expect(hems_jwt)
    @hems_ns.marshal_with(hems_jwt)
    def post(self):
        """Generate a new JWT"""
        incoming_jwt = hems_ns.payload["jwt"]
        try:
            decoded_jwt = jwt.decode(
                incoming_jwt, f"{SHARED_SECRET}{MAC_ADDRESS}", algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError as error:
            return error

        if decoded_jwt.get("authorized"):
            current_app.jwt = current_app.config["HEMSDAO"].generate_new_jwt()
            return {'jwt': current_app.jwt}, HTTPStatus.OK
        else:
            return HTTPStatus.UNAUTHORIZED
