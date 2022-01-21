from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
from state import load_state, save_state
from operator import itemgetter

api = Namespace('home', description='Home Operations')
lpc_config = api.model("LPC Config", {
        "name": fields.String(description="LPC name"),
        "status_communication": fields.Boolean(description="Whether the home is communicating"),
        "technical_contact": fields.String(description="Technical contact phone/email/phone and email"),
        "technical_phone": fields.String(description="Technical contact phone number"),
        "technical_email": fields.String(description="Technical contact email"),
        })

home = api.model('Home', {
    'id': fields.String(readonly=True, description='The Home unique identifier'),
    "lpc_config": fields.Nested(lpc_config)
})

class HomeDAO(object):
    def __init__(self, home=None):
        self.home = home
        
    def get(self):
        if self.home is None:
            api.abort(HTTPStatus.NOT_FOUND, f"home doesn't exist")    
        return self.home

    def create(self, data):
        self.home = data
        return home

    def update(self, data):
        self.home.update(data)
        return home

    def delete(self):
        self.home = None

state = load_state()
DAO = HomeDAO(state.get("home", None))

@api.route('/')
class Home(Resource):
    @api.doc('create_home')
    @api.expect(home)
    @api.marshal_with(home, envelope='home', code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new home'''
        myDevice = DAO.create(api.payload)
        state["home"] = DAO.get()
        save_state(state)
        return myDevice, HTTPStatus.CREATED

@api.route('/config')
class Config(Resource):
    '''Shows home configuration'''
    @api.doc('home_config')
    @api.marshal_list_with(home, envelope='home', skip_none=True)
    @jwt_required()
    def get(self):
        '''Get home configuration'''
        return DAO.get(), HTTPStatus.OK