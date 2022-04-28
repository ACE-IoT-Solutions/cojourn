from api_mock.apis.namespace import auth_ns
from flask_restx import fields

token = auth_ns.model("Token", {
    "access_token": fields.String(readonly=True)
})

login_fields = auth_ns.model("User", {
    "email": fields.String,
    "password": fields.String
})
