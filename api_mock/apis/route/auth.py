from http import HTTPStatus

from api_mock.apis.dao.auth_dao import AuthDAO
from api_mock.apis.model.auth import login_fields, token
from api_mock.apis.namespace import auth_ns
from flask_jwt_extended import jwt_required
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource


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
