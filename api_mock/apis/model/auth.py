from datetime import timedelta
from flask_restx import Resource, fields
from flask_restx.namespace import Namespace
from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api_mock.apis.namespace import auth_ns


token = auth_ns.model("Token", {
    "access_token": fields.String(readonly=True)
})

login_fields = auth_ns.model("User", {
    "email": fields.String,
    "password": fields.String
})
