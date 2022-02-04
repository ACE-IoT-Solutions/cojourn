import json
from random import sample
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus

import jwt
from api_mock.apis.dao.device_dao import DeviceDAO
from api_mock.apis.model.device import (
    device,
    thermostat,
    water_heater,
    home_battery,
    ev_charger,
    pv_system,
    generation_sample
    )
from state import load_state, save_state

from api_mock.apis.types import (
    DemandResponseStatus,
    DeviceStatus,
    DeviceService,
    ThermostatMode,
    Weather,
    ChargeRate,
    DeviceType,
)
from api_mock.apis.namespace import device_ns

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
