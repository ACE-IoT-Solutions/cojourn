import os
import tempfile
import pytest
import json

from api_mock import create_app
from .support import authenticated_client

thermostat_data = {
    "id": "e4d197aa-fa13-4255-b395-63268be12515",
    "name": "Living Room",
    "type": "thermostat",
    "location": "Living Room",
    "status": "on",
    "provisioned": True,
}

def test_device_list(authenticated_client):
    response = authenticated_client.get("/api/v1/devices/")
    device_data = json.loads(response.data)

    assert device_data[0] == thermostat_data

def test_device_endpoints(authenticated_client):
    response = authenticated_client.get("/api/v1/devices/e4d197aa-fa13-4255-b395-63268be12515")
    device_data = json.loads(response.data)

    assert device_data["device"] == thermostat_data
