from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
from state import load_state, save_state
from operator import itemgetter
from api_mock.apis.model.home import home
from api_mock.apis.namespace import home_ns

class HomeDAO(object):
    def __init__(self, home=None):
        self.home = home
        
    def get(self):
        if self.home is None:
            home_ns.abort(HTTPStatus.NOT_FOUND, f"home doesn't exist")    
        return self.home

    def create(self, data):
        self.home = data
        return home

    def update(self, data):
        self.home.update(data)
        return home

    def delete(self):
        self.home = None