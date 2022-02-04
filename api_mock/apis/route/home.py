from http import HTTPStatus

from api_mock.apis.dao.home_dao import HomeDAO
from api_mock.apis.model.home import home
from api_mock.apis.namespace import home_ns
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from state import load_state, save_state


state = load_state()
DAO = HomeDAO(state.get("home", None))


@home_ns.route('/')
class Home(Resource):
    @home_ns.doc('create_home')
    @home_ns.expect(home)
    @home_ns.marshal_with(home, envelope='home', code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new home'''
        myDevice = DAO.create(home_ns.payload)
        state["home"] = DAO.get()
        save_state(state)
        return myDevice, HTTPStatus.CREATED


@home_ns.route('/config')
class Config(Resource):
    '''Shows home configuration'''
    @home_ns.doc('home_config')
    @home_ns.marshal_list_with(home, envelope='home', skip_none=True)
    @jwt_required()
    def get(self):
        '''Get home configuration'''
        return DAO.get(), HTTPStatus.OK
