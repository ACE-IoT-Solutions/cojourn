from http import HTTPStatus
from typing import List, Protocol, Tuple, Union
from abc import abstractmethod

from api_mock.apis.types import ThermostatMode


class HomeProtocol(Protocol):
    @abstractmethod
    def __init__(self, home: dict=None) -> any:
        ...

    @abstractmethod
    def get(self) -> dict:
        ...

    @abstractmethod
    def create(self, data: dict) -> dict:
        ...

    @abstractmethod
    def update(self, data: dict) -> dict:
        ...

    @abstractmethod
    def delete(self) -> any:
        ...
        
