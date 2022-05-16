from typing import Protocol, Union
from http import HTTPStatus
from abc import abstractmethod

class AuthProtocol(Protocol):
    @abstractmethod
    def __init__(self) -> any:
        ...
    
    @abstractmethod
    def login(self, data: dict) -> Union[dict, HTTPStatus]:
        ...
    
    @abstractmethod
    def logout(self) -> any:
        ...