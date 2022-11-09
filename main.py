from optparse import OptionParser
import logging
from cojourn.api_mock import create_app


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

    app = create_app("ProductionConfig")
    app.run(host=options.host, port=options.port, debug=True)


if __name__ == "__main__":
    main()
