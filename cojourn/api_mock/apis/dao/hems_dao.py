from datetime import timedelta
from http import HTTPStatus
from cojourn.api_mock.apis.protocols import HEMSProtocol

from cojourn.api_mock.apis.namespace import hems_ns
from flask import current_app
import jwt

class HEMSDAO(HEMSProtocol):
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

    def generate_new_jwt(self):
        jwt_data = {'sub': "1234567890", 'name': "John Doe", 'iat': 1516239022}
        encoded_jwt = jwt.encode(jwt_data, "super secret", algorithm="HS256")
        self.hems['jwt'] = encoded_jwt
        return encoded_jwt

    def set_der_status(self, id, status):
        if self.hems["id"] != id:
            hems_ns.abort(HTTPStatus.NOT_FOUND, f"HEMS with id {id} doesn't exist")
        
        self.hems["dr_status"] = status
        return current_app.config["DeviceDAO"].set_all_der_status(status)

    def delete(self):
        self.hems = None
