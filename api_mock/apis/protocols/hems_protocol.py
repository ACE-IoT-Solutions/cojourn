from http import HTTPStatus
from typing import List, Protocol, Tuple, Union
from abc import abstractmethod

from api_mock.apis.types import ThermostatMode


class HEMSProtocol(Protocol):
    @abstractmethod
    def __init__(self, hems: dict=None) -> any:
        ...
    
    @abstractmethod  
    def get(self) -> Union[dict, Tuple[HTTPStatus, str]]:
        ...
    
    @abstractmethod
    def get_id(self, id) -> Union[dict, Tuple[HTTPStatus, str]]:
        ...

    @abstractmethod
    def create(self, data: dict) -> dict:
        ...

    @abstractmethod
    def update(self, data: dict) -> dict:
        ...

    @abstractmethod
    def set_der_status(self, id: str, status: str) -> Union[List[dict], Tuple[HTTPStatus, str]]:
        ...

    @abstractmethod
    def delete(self) -> any:
        ...