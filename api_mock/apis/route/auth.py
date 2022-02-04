from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
from state import load_state, save_state
from operator import itemgetter
from api_mock.apis.model.home import home
from api_mock.apis.dao.home_dao import HomeDAO
from api_mock.apis.namespace import home_ns
from datetime import timedelta
from flask_restx import Resource, fields
from flask_restx.namespace import Namespace
from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api_mock.apis.model.auth import token, login_fields
from api_mock.apis.dao.auth_dao import AuthDAO
from api_mock.apis.namespace import auth_ns
from state import load_state


# auth_ns = Namespace('auth', description='Authentication Operations')
AuthDAO = AuthDAO()


@auth_ns.route("/login")
class AuthLogin(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_fields)
    @auth_ns.marshal_with(token)
    def post(self):
        '''Login'''
        return AuthDAO.login(auth_ns.payload), HTTPStatus.OK
        
    
@auth_ns.route("/logout")
class AuthLogin(Resource):
    @auth_ns.doc('logout')
    @jwt_required()
    def post(self):
        AuthDAO.logout()
        return HTTPStatus.OK