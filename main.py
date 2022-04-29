from optparse import OptionParser
from api_mock import create_app
import logging

from http import HTTPStatus
from api_mock.apis.protocols import AuthProtocol

from api_mock.apis.namespace import auth_ns
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta


class myDAO(AuthProtocol):
    def __init__(self):
        self.tokens = []

    @auth_ns.doc(security=[])
    def login(self, data):
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        self.tokens.append(token)
        return {"access_token": token}

    def logout(self):
        try:
            self.tokens.remove(get_jwt_identity())
        except ValueError:
            auth_ns.abort
            return HTTPStatus.NOT_FOUND


def set_simulator(options, opt_str, value, parser):
    parser.values.host = "127.0.0.1"
    parser.values.port = "5000"


def set_lan(options, opt_str, value, parser):
    parser.values.host = "0.0.0.0"
    parser.values.port = "80"


def main():
    parser = OptionParser()
    parser.add_option("--host", dest="host", default="127.0.0.1",
                      help="Hostname", metavar="HOST")
    parser.add_option("--port", dest="port", default=5000,
                      help="port", metavar="PORT")
    parser.add_option("--simulator", action="callback",
                      callback=set_simulator, nargs=0)
    parser.add_option("--lan", action="callback", callback=set_lan, nargs=0)

    (options, args) = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    app = create_app("ProductionConfig", myDAO())
    app.run(host=options.host, port=options.port, debug=True)


if __name__ == "__main__":
    main()
