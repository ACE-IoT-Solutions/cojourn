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

car_charger_data = {
    "id": "f8204550-32cc-44aa-bf48-a95a90c1504f",
    "name": "Linda's Charger",
    "type": "car_charger",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
}

solar_panels_data = {
    "id": "8b98e3cf-af15-4ead-8d5e-a2d389723a25",
    "name": "Solar Energy",
    "type": "solar_panels",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
}

water_heater_data = {
    "id": "a3f67bfe-0b41-4054-889e-fa1d6c5d93d1",
    "name": "Water Heater",
    "type": "water_heater",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
}

home_battery_data = {
    "id": "052fe39f-5439-4682-beca-b10f2ea00113",
    "name": "Home Battery",
    "type": "home_battery",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
}

def test_device_list(authenticated_client):
    response = authenticated_client.get("/api/v1/devices/")
    device_data = json.loads(response.data)

    assert isinstance(device_data, dict)
    assert device_data['devices'] == [thermostat_data, car_charger_data, solar_panels_data, water_heater_data, home_battery_data]

def test_device_endpoints(authenticated_client):
    thermostat_response = authenticated_client.get("/api/v1/devices/e4d197aa-fa13-4255-b395-63268be12515")
    thermostat_response_data = json.loads(thermostat_response.data)
    assert thermostat_response_data["device"] == thermostat_data

    car_charger_response = authenticated_client.get("/api/v1/devices/f8204550-32cc-44aa-bf48-a95a90c1504f")
    car_charger_response_data = json.loads(car_charger_response.data)
    assert car_charger_response_data["device"] == car_charger_data

    solar_panels_response = authenticated_client.get("/api/v1/devices/8b98e3cf-af15-4ead-8d5e-a2d389723a25")
    solar_panels_response_data = json.loads(solar_panels_response.data)
    assert solar_panels_response_data["device"] == solar_panels_data
    
    water_heater_response = authenticated_client.get("/api/v1/devices/a3f67bfe-0b41-4054-889e-fa1d6c5d93d1")
    water_heater_response_data = json.loads(water_heater_response.data)
    assert water_heater_response_data["device"] == water_heater_data

    home_battery_response = authenticated_client.get("/api/v1/devices/052fe39f-5439-4682-beca-b10f2ea00113")
    home_battery_response_data = json.loads(home_battery_response.data)
    assert home_battery_response_data["device"] == home_battery_data