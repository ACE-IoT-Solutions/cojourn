from http import HTTPStatus

from cojourn.api_mock.apis.dao import HomeDAO
from cojourn.api_mock.apis.model.home import home
from cojourn.api_mock.apis.namespace import home_ns
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from flask import current_app
from cojourn.state import load_state, save_state

state = load_state()

@home_ns.route('/')
class Home(Resource):
    @home_ns.doc('create_home')
    @home_ns.expect(home)
    @home_ns.marshal_with(home, envelope='home', code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new home'''
        myDevice = current_app.config["HomeDAO"].create(home_ns.payload)
        state["home"] = current_app.config["HomeDAO"].get()
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
        return current_app.config["HomeDAO"].get(), HTTPStatus.OK
