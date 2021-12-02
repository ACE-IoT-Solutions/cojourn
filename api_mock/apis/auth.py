from datetime import timedelta
from flask_restx import Resource, fields
from flask_restx.namespace import Namespace
from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Namespace("auth", "API authentication operations")

token = api.model("Token", {
    "access_token": fields.String(readonly=True)
})

login_fields = api.model("User", {
    "email": fields.String,
    "password": fields.String
})


class AuthDAO(object):
    def __init__(self):
        self.tokens = []
    
    @api.doc(security=[])
    def login(self, data):
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        self.tokens.append(token)
        return {"access_token": token}
        
    def logout(self):
        try:
            self.tokens.remove(get_jwt_identity())
        except ValueError:
            api.abort
            return HTTPStatus.NOT_FOUND
            
        
AuthDAO = AuthDAO()

@api.route("/login")
class AuthLogin(Resource):
    @api.expect(login_fields)
    @api.marshal_with(token)
    def post(self):
        return AuthDAO.login(api.payload), HTTPStatus.OK
        
    
@api.route("/logout")
class AuthLogin(Resource):
    @jwt_required()
    def post(self):
        AuthDAO.logout()
        return HTTPStatus.OK