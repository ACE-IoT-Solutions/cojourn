from http import HTTPStatus

from api_mock.apis.model.home import home
from api_mock.apis.namespace import home_ns
from api_mock.apis.protocols.home_protocol import HomeProtocol


class HomeDAO(HomeProtocol):
    def __init__(self, home=None):
        self.home = home
        

    def get(self):
        if self.home is None:
            home_ns.abort(HTTPStatus.NOT_FOUND, f"home doesn't exist")
        return self.home

    def create(self, data):
        self.home = data
        return home

    def update(self, data):
        self.home.update(data)
        return home

    def delete(self):
        self.home = None
