import json
from random import sample
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus

import jwt
from state import load_state, save_state

from .types import (
    DemandResponseStatus,
    DeviceStatus,
    DeviceService,
    ThermostatMode,
    Weather,
    ChargeRate,
    DeviceType,
)

device_ns = Namespace("devices", description="Device Operations")

device = device_ns.model(
    "Device",
    {
        "id": fields.String(required=True, description="The Device unique identifier"),
        "name": fields.String(required=True, description="The Device's Name"),
        "type": fields.String(
            required=True,
            enum=[device_type for device_type in DeviceType],
            description="The Device's Type",
        ),
        "location": fields.String(required=True, description="The Device's Location"),
        "provisioned": fields.Boolean(
            required=True, description="The Device's Provisioned Status"
        ),
        "status": fields.String(
            required=True,
            description="The Device's Status",
            enum=[status for status in DeviceStatus],
        ),
        "dr_status": fields.String(
            required=True,
            description="Demand Response Status",
            enum=[status for status in DemandResponseStatus],
        ),
    },
)

# create thermostat api model
# Thermostat
thermostat = device_ns.inherit(
    "Thermostat",
    device,
    {
        "mode": fields.String(
            required=False,
            enum=[mode for mode in ThermostatMode],
            description="Thermostat Current Mode",
        ),
        "setpoint": fields.Fixed(
            decimals=2, required=False, description="Thermostat target temperature (C)"
        ),
        "setpoint_span": fields.Fixed(
            decimals=2, required=False, description="Thermostat setpoint span (C)"
        ),
        "interior_temperature": fields.Fixed(
            decimals=2, required=False, description="Thermostat Current Temperature (C)"
        ),
        "exterior_temperature": fields.Fixed(
            decimals=2,
            required=False,
            description="Thermostat Exterior Temperature (C)",
        ),
        "exterior_weather": fields.String(
            required=False,
            enum=[weather for weather in Weather],
            description="Weather description",
        ),
    },
)

generation_sample = device_ns.model(
    "Generation Sample",
    {
        "name": fields.String(readOnly=True, description="The Device's Name"),
        "timestamp": fields.DateTime(
            readOnly=True, description="Timestamp of the sample"
        ),
        "power_generated": fields.Fixed(
            readOnly=True, decimals=2, description="Power Generated (wH)"
        ),
        "power_sent_to_grid": fields.Fixed(
            readonly=True, decimals=2, description="Power Sent to Grid (wH)"
        ),
    },
)

list_of_generation_samples = device_ns.model(
    "List of Generation Samples",
    {"samples": fields.List(fields.Nested(generation_sample))},
)

# Solar Panels
pv_system = device_ns.inherit(
    "Photovoltaic Systems",
    device,
    {
        "label": fields.String(
            required=False,
            description="The Device's Status (deprecated)",
            enum=[status for status in DeviceStatus],
        ),
        "power_generated_this_month": fields.Fixed(
            readOnly=True, decimals=2, description="Power Generated This Month (wH)"
        ),
        "power_sent_to_grid_this_month": fields.Fixed(
            readOnly=True, decimals=2, description="Power Sent to Grid This Month (wH)"
        ),
        "generation_samples": fields.Nested(list_of_generation_samples),
    },
)

pv_systems = device_ns.model(
    "List of Photovoltaic Systems",
    {"solar_panels": fields.List(fields.Nested(pv_system))},
)

# Home Battery
home_battery = device_ns.inherit(
    "Home Battery",
    device,
    {
        "reserve_limit": fields.Fixed(
            decimals=2, required=False, description="Home Battery Reserve Limit %"
        ),
        "service": fields.String(
            required=False,
            enum=[service for service in DeviceService],
            description="Service description",
        ),
        "charge_percentage": fields.Fixed(
            decimals=2, required=False, description="The Device's Charge Amount %"
        ),
        "charge_rate": fields.String(
            required=False,
            enum=[c for c in ChargeRate],
            description="The Device's Charge Rate",
        ),
    },
)

ev_charger = device_ns.inherit(
    "EV Charger",
    device,
    {
        "service": fields.String(
            required=False,
            enum=[service for service in DeviceService],
            description="Service description",
        ),
        "charge_percentage": fields.Fixed(
            decimals=2, required=False, description="The Device's Charge Amount %"
        ),
        "charge_rate": fields.String(
            required=False,
            enum=[c for c in ChargeRate],
            description="The Device's Charge Rate",
        ),
    },
)

# Shared
water_heater = device_ns.inherit(
    "Water Heater",
    device,
    {
        "label": fields.String(
            required=False,
            description="The Device's Status (deprecated)",
            enum=[status for status in DeviceStatus],
        ),
        "service": fields.String(
            required=False,
            enum=[service for service in DeviceService],
            description="Service description",
        ),
    },
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
        if data["mode"] not in ThermostatMode:
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
        if data["charge_rate"] not in ChargeRate:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST,
                f"ev charger charge rate {data['charge_rate']} is not valid",
            )
        device["charge_rate"] = data["charge_rate"]
        device.update(device)
        device.update(self.__decorate_device(device))
        return device

    def home_battery_reserve_limit_update(self, id, data):
        device = self.get_by_type(id, "home_battery")
        device["reserve_limit"] = data["reserve_limit"]
        device.update(device)
        device.update(self.__decorate_device(device))
        return device

    def delete(self, id):
        device = self.get(id)
        self.devices.remove(device)


state = load_state()
DAO = DeviceDAO(state.get("devices", []))


@device_ns.route("/")
class DeviceList(Resource):
    """Shows a list of all devices"""

    @device_ns.doc("list_devices")
    @device_ns.marshal_list_with(device, envelope="devices", skip_none=True)
    @jwt_required()
    def get(self):
        """List all devices"""
        return DAO.get_list(), HTTPStatus.OK

    @device_ns.doc("create_device")
    @device_ns.expect(device)
    @device_ns.marshal_with(device, envelope="device", code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        """Create a new device"""
        myDevice = DAO.create(device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.CREATED


@device_ns.route("/<string:id>")
class Device(Resource):
    """Get device by id"""

    @device_ns.doc("get device by id")
    # @device_ns.marshal_with(device, envelope='device', skip_none=True)
    @jwt_required()
    def get(self, id):
        """get device by id"""
        return DAO.get(id), HTTPStatus.OK

    @device_ns.doc("Update device")
    @device_ns.expect(device)
    @device_ns.marshal_with(device, envelope="device", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update device state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.THERMOSTAT}/<string:id>")
class Thermostat(Resource):
    """Get Thermostat"""

    @device_ns.doc("get thermostat by id")
    @device_ns.marshal_with(thermostat, envelope=DeviceType.THERMOSTAT, skip_none=True)
    @jwt_required()
    def get(self, id):
        """get thermostat by id"""
        device = DAO.get(id)
        if device.get("type") != DeviceType.THERMOSTAT:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {id} is not a {DeviceType.THERMOSTAT}"
            )
        return device, HTTPStatus.OK

    @device_ns.doc("Update thermostat")
    @device_ns.expect(thermostat)
    @device_ns.marshal_with(thermostat, envelope="thermostat", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update thermostat state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.WATER_HEATER}/<string:id>")
class WaterHeater(Resource):
    """Get Water Heater"""

    @device_ns.doc("get water_heater by id")
    @device_ns.marshal_with(water_heater, envelope="water_heater", skip_none=True)
    @jwt_required()
    def get(self, id):
        """get water_heater by id"""
        device = DAO.get(id)
        if device.get("type") != DeviceType.WATER_HEATER:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {id} is not a water_heater"
            )
        return device, HTTPStatus.OK

    @device_ns.doc("Update water_heater")
    @device_ns.expect(water_heater)
    @device_ns.marshal_with(water_heater, envelope="water_heater", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update water_heater state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.HOME_BATTERY}/<string:id>")
class HomeBattery(Resource):
    """Get Home Battery"""

    @device_ns.doc("get home_battery by id")
    @device_ns.marshal_with(home_battery, envelope="home_battery", skip_none=True)
    @jwt_required()
    def get(self, id):
        """get home_battery by id"""
        device = DAO.get(id)
        if device.get("type") != DeviceType.HOME_BATTERY:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {id} is not a home_battery"
            )
        return device, HTTPStatus.OK

    @device_ns.doc("Update home_battery")
    @device_ns.expect(home_battery)
    @device_ns.marshal_with(home_battery, envelope="home_battery", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update home_battery state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


home_battery_reserve_limit = device_ns.model(
    "HomeBatteryReserveLimit", {"reserve_limit": fields.Integer}
)


@device_ns.route(f"/{DeviceType.HOME_BATTERY}/<string:id>/update_reserve_limit")
class HomeBatteryReserveLimit(Resource):
    """Update Home Battery Reserve Limit"""

    @device_ns.doc("update home_battery reserve limit")
    @device_ns.expect(home_battery_reserve_limit)
    @device_ns.marshal_with(home_battery, envelope="home_battery", code=HTTPStatus.OK)
    @jwt_required()
    def post(self, id):
        """update home_battery reserve limit"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        updated_device = DAO.home_battery_reserve_limit_update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return updated_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.EV_CHARGER}/<string:id>")
class EVCharger(Resource):
    """Get EV Charger"""

    @device_ns.doc("get ev_charger by id")
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", skip_none=True)
    @jwt_required()
    def get(self, id):
        """get ev_charger by id"""
        device = DAO.get(id)
        if device.get("type") != DeviceType.EV_CHARGER:
            device_ns.abort(HTTPStatus.BAD_REQUEST, f"device {id} is not a ev_charger")
        return device, HTTPStatus.OK

    @device_ns.doc("Update ev_charger")
    @device_ns.expect(ev_charger)
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update ev_charger state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


ev_charge_rate = device_ns.model(
    "EVChargeRate",
    {
        "charge_rate": fields.String(
            required=True,
            enum=[val for val in ChargeRate],
            description="EV charge rate",
        )
    },
)


@device_ns.route(f"/{DeviceType.EV_CHARGER}/<string:id>/update_charge_rate")
class UpdateEVChargeRate(Resource):
    """Update EV Charger Charge Rate"""

    @device_ns.doc("update ev_charger charge rate")
    @device_ns.expect(ev_charge_rate)
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", code=HTTPStatus.OK)
    @jwt_required()
    def post(self, id):
        """update ev_charger charge rate"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.ev_charge_rate_update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.PV_SYSTEM}/<string:id>")
class PVSystem(Resource):
    """Get PV System"""

    @device_ns.doc("get pv_system by id")
    @device_ns.marshal_with(pv_system, envelope="pv_system", skip_none=True)
    @jwt_required()
    def get(self, id):
        """get pv_system by id"""
        device = DAO.get(id)
        if device.get("type") != DeviceType.PV_SYSTEM:
            device_ns.abort(HTTPStatus.BAD_REQUEST, f"device {id} is not a pv_system")
        return device, HTTPStatus.OK

    @device_ns.doc("Update pv_system")
    @device_ns.expect(pv_system)
    @device_ns.marshal_with(pv_system, envelope="pv_system", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        """update pv_system state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.PV_SYSTEM}/<string:id>/generation")
class PVSystemGeneration(Resource):
    """Get timeseries generation data for solar panels"""

    @device_ns.doc("get timeseries generation data for solar panels")
    @device_ns.marshal_list_with(
        generation_sample, envelope="generation_samples", skip_none=True
    )
    @jwt_required()
    def get(self, id: str):
        """get timeseries generation data for solar panels"""
        return self.get_timeseries(id)

    def get_timeseries(self, device_id: str):
        device = DAO.get(device_id)
        if (
            device.get("generation_samples") != []
            and device.get("generation_samples") is not None
        ):
            device_samples = list(
                map(
                    lambda sample: {"name": device["name"], **sample},
                    device["generation_samples"],
                )
            )

            if device_samples is not None and device_samples != []:
                return device_samples, HTTPStatus.OK
        else:
            return None, HTTPStatus.NOT_FOUND


temperature_params = device_ns.model(
    "TemperatureParams",
    {
        "setpoint": fields.Fixed(
            decimals=2, required=False, description="Thermostat target temperature (C)"
        ),
        "mode": fields.String(
            required=False,
            enum=[mode for mode in ThermostatMode],
            description="Thermostat Current Mode",
        ),
    },
)


@device_ns.route(f"/{DeviceType.THERMOSTAT}/<string:id>/update_setpoint")
class Device(Resource):
    @device_ns.expect(temperature_params)
    @device_ns.doc("Set thermostat temperature")
    @jwt_required()
    def post(self, id):
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        device = DAO.get(id)
        if device["type"] != "thermostat":
            return f"Cannot set temperature on {device.type}", HTTPStatus.BAD_REQUEST

        updatedDevice = DAO.thermostat_setpoint_update(id, device_ns.payload)
        state["devices"] = DAO.get_list()
        save_state(state)

        return updatedDevice, HTTPStatus.OK
