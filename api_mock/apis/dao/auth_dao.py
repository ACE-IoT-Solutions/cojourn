from datetime import timedelta
from flask_restx import Resource, fields
from flask_restx.namespace import Namespace
from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api_mock.apis.model.auth import token, login_fields
from api_mock.apis.namespace import auth_ns


class AuthDAO(object):
    def __init__(self):
        self.tokens = []
    
    @auth_ns.doc(security=[])
    def login(self, data):
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        self.tokens.append(token)
        return {"access_token": token}
        
    def logout(self):
        try:
            self.tokens.remove(get_jwt_identity())
        except ValueError:
            auth_ns.abort
            return HTTPStatus.NOT_FOUND
            