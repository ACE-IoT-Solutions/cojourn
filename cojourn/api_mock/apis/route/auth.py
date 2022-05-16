from http import HTTPStatus

from cojourn.api_mock.apis.model.auth import login_fields, token
from cojourn.api_mock.apis.namespace import auth_ns
from flask_jwt_extended import jwt_required
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from flask import current_app


@auth_ns.route("/login")
class AuthLogin(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_fields)
    @auth_ns.marshal_with(token)
    def post(self):
        '''Login'''
        return current_app.config["AuthDAO"].login(auth_ns.payload), HTTPStatus.OK


@auth_ns.route("/logout")
class AuthLogin(Resource):
    @auth_ns.doc('logout')
    @jwt_required()
    def post(self):
        current_app.config["AuthDAO"].logout()
        return HTTPStatus.OK
