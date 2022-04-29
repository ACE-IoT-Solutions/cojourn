from http import HTTPStatus
from typing import List, Protocol, Tuple, Union
from abc import abstractmethod

from api_mock.apis.types import ThermostatMode


class DeviceProtocol(Protocol):
    @abstractmethod
    def _thermostat_setpoint_span(self, mode: ThermostatMode) -> ThermostatMode:
        ...
    
    @abstractmethod
    def _decorate_device(self, device: dict) -> dict:
        ...

    @abstractmethod
    def __init__(self, devices: List[dict]=[]):
        ...

    @abstractmethod
    def get_list(self) -> List[dict]:
        ...

    @abstractmethod
    def get(self, id:str) -> Union[dict, Tuple[HTTPStatus, str]]:
        ...

    @abstractmethod
    def get_by_type(self, id: str, type: str) -> Union[dict, Tuple[HTTPStatus, str]]:
        ...

    @abstractmethod
    def create(self, data: dict) -> dict:
        ...

    @abstractmethod
    def update(self, id: str, data: dict) -> dict:
        ...

    @abstractmethod
    def update_by_type(self, id: str, data: dict, type: str) -> dict:
        ...

    @abstractmethod
    def thermostat_setpoint_update(self, id: str, data: dict) -> dict:
        ...

    @abstractmethod
    def ev_charge_rate_update(self, id: str, data: dict) -> dict:
        ...
    
    @abstractmethod
    def set_der_status(self, id: str, status: str) -> dict:
        ...

    @abstractmethod
    def set_all_der_status(self, status: str) -> List[dict]:
        ...

    @abstractmethod
    def home_battery_reserve_limit_update(self, id: str, data: dict) -> dict:
        ...

    @abstractmethod
    def home_battery_charge_rate_update(self, id: str, data: dict):
        ...

    @abstractmethod
    def delete(self, id: str) -> any:
        ...
        
