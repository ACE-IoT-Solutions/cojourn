from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restx import fields, Namespace, Resource
from api_mock.apis.dao.device_dao import DeviceDAO
from api_mock.apis.namespace import hems_ns


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
        return DeviceDAO.set_all_der_status(status)
        

    def delete(self):
        self.home = None

    

