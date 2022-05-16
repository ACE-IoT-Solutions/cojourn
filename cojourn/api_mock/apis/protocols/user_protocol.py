from http import HTTPStatus
from typing import List, Protocol, Tuple, Union
from abc import abstractmethod

from cojourn.api_mock.apis.types import ThermostatMode


class UserProtocol(Protocol):
    pass