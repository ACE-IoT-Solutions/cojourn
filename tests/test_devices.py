import os
import tempfile
import pytest
import json

from cojourn.api_mock import create_app
from .support import authenticated_client, load_fixture

thermostat_data = load_fixture('devices/thermostat.json')
car_charger_data = load_fixture('devices/car_charger.json')
solar_panels_data = load_fixture('devices/solar_panels.json')
water_heater_data = load_fixture('devices/water_heater.json')
home_battery_data = load_fixture('devices/home_battery.json')

def test_device_list(authenticated_client):
    response = authenticated_client.get("/api/v1/devices/")
    assert json.loads(response.data) == load_fixture('devices.json')

def test_device_endpoints(authenticated_client):
    thermostat_response = authenticated_client.get("/api/v1/devices/e4d197aa-fa13-4255-b395-63268be12515")
    thermostat_response_data = json.loads(thermostat_response.data)
    assert thermostat_response_data == thermostat_data

    car_charger_response = authenticated_client.get("/api/v1/devices/f8204550-32cc-44aa-bf48-a95a90c1504f")
    car_charger_response_data = json.loads(car_charger_response.data)
    assert car_charger_response_data == car_charger_data

    solar_panels_response = authenticated_client.get("/api/v1/devices/8b98e3cf-af15-4ead-8d5e-a2d389723a25")
    solar_panels_response_data = json.loads(solar_panels_response.data)
    assert solar_panels_response_data == solar_panels_data
    
    water_heater_response = authenticated_client.get("/api/v1/devices/a3f67bfe-0b41-4054-889e-fa1d6c5d93d1")
    water_heater_response_data = json.loads(water_heater_response.data)
    assert water_heater_response_data == water_heater_data

    home_battery_response = authenticated_client.get("/api/v1/devices/052fe39f-5439-4682-beca-b10f2ea00113")
    home_battery_response_data = json.loads(home_battery_response.data)
    assert home_battery_response_data == home_battery_data
