import json
from random import sample
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus

import jwt
from state import load_state, save_state
from api_mock.apis.namespace import device_ns

from api_mock.apis.types import (
    DemandResponseStatus,
    DeviceStatus,
    DeviceService,
    ThermostatMode,
    Weather,
    ChargeRate,
    DeviceType,
)


class DeviceDAO(object):
    def __thermostat_setpoint_span(self, mode: ThermostatMode):
        return {
            ThermostatMode.AUTO: 2,
            ThermostatMode.HEAT: 2,
            ThermostatMode.COOL: 2,
            ThermostatMode.ECO: 4,
            ThermostatMode.OFF: 0,
        }[mode]

    def __decorate_device(self, device):
        if device["type"] == "thermostat":
            device_mode = ThermostatMode(device["mode"])
            device["setpoint_span"] = self.__thermostat_setpoint_span(device_mode)

        return device

    def __init__(self, devices=[]):
        self.devices = list(map(self.__decorate_device, devices))

    def get_list(self):
        return self.devices

    def get(self, id):
        for device in self.devices:
            if device["id"] == id:
                return device
        device_ns.abort(HTTPStatus.NOT_FOUND, f"device {id} doesn't exist")

    def get_by_type(self, id, type):
        for device in self.devices:
            if device["id"] == id and device["type"] == type:
                return device
        device_ns.abort(
            HTTPStatus.NOT_FOUND, f"device {id} doesn't exist or is not of type {type}"
        )

    def create(self, data):
        device = data
        device["id"] = data["id"]
        self.devices.append(device)
        return device

    def update(self, id, data):
        device = self.get(id)
        device.update(data)
        device.update(self.__decorate_device(device))
        return device

    def update_by_type(self, id, data, type):
        device = self.get(id)
        if device["type"] != type:
            device_ns.abort(
                HTTPStatus.NOT_FOUND,
                f"device {id} doesn't exist or is not of type {type}",
            )
        device.update(data)
        device.update(self.__decorate_device(device))
        return device

    def thermostat_setpoint_update(self, id, data):
        device = self.get_by_type(id, "thermostat")
        if data["mode"] not in set(mode.value for mode in ThermostatMode):
            device_ns.abort(
                HTTPStatus.BAD_REQUEST,
                f"thermostat mode {data['mode']} is not valid",
            )
        device["mode"] = data["mode"]
        device["setpoint"] = data["setpoint"]
        device.update(device)
        device.update(self.__decorate_device(device))
        return device

    def ev_charge_rate_update(self, id, data):
        device = self.get_by_type(id, "ev_charger")
        
        if data["charge_rate"] not in set(charge_rate.value for charge_rate in ChargeRate):
            device_ns.abort(
                HTTPStatus.BAD_REQUEST,
                f"ev charger charge rate {data['charge_rate']} is not valid",
            )
        device["charge_rate"] = data["charge_rate"]
        device.update(device)
        device.update(self.__decorate_device(device))
        return device
    
    def set_all_der_status(self, status):
        for device in self.devices:
            if "dr_status" in device:
                device["dr_status"] = status
        return self.devices

    def home_battery_reserve_limit_update(self, id, data):
        device = self.get_by_type(id, "home_battery")
        device["reserve_limit"] = data["reserve_limit"]
        device.update(device)
        device.update(self.__decorate_device(device))
        return device

    def delete(self, id):
        device = self.get(id)
        self.devices.remove(device)