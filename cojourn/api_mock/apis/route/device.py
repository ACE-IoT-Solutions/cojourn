from http import HTTPStatus

from cojourn.api_mock.apis.model.device import (
    device,
    ev_charger,
    generation_sample,
    home_battery,
    pv_system,
    thermostat,
    water_heater,
)
from cojourn.api_mock.apis.namespace import device_ns
from cojourn.api_mock.apis.types import ChargeRate, DeviceType, ThermostatMode
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource, fields, Namespace

from time import sleep
import jwt
from cojourn.state import load_state, save_state
from datetime import datetime

from cojourn.api_mock.apis.types import (
    DemandResponseStatus,
    DeviceStatus,
    DeviceService,
    ThermostatMode,
    Weather,
    ChargeRate,
    DeviceType,
)
from cojourn.api_mock.apis.namespace import device_ns
from cojourn.api_mock.apis.model.device import (
    device_der_status,
    usage_sample,
    home_battery_reserve_limit,
    home_battery_charge_rate,
    ev_charge_rate,
    temperature_params,
)
from flask import current_app

state = load_state()


@device_ns.route("/")
class DeviceList(Resource):
    """Shows a list of all devices"""

    @device_ns.doc("list_devices")
    @device_ns.marshal_list_with(device, envelope="devices", skip_none=True)
    @jwt_required()
    def get(self):
        """List all devices"""
        return current_app.config["DeviceDAO"].get_list(), HTTPStatus.OK

    @device_ns.doc("create_device")
    @device_ns.expect(device)
    @device_ns.marshal_with(device, envelope="device", code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        """Create a new device"""
        my_device = current_app.config["DeviceDAO"].create(device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.CREATED


@device_ns.route("/<string:device_id>")
class Device(Resource):
    """Get device by id"""

    @device_ns.doc("get device by id")
    # @device_ns.marshal_with(device, envelope='device', skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get device by id"""
        sleep(1)
        return current_app.config["DeviceDAO"].get(device_id), HTTPStatus.OK

    @device_ns.doc("Update device")
    @device_ns.expect(device)
    @device_ns.marshal_with(device, envelope="device", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update device state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route("/<string:device_id>/set_der_status")
class Device(Resource):
    @device_ns.doc("Update device DR status")
    @device_ns.expect(device_der_status)
    @jwt_required()
    def post(self, device_id):
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].set_der_status(
            device_id, device_ns.payload["status"]
        )
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.THERMOSTAT}/<string:device_id>")
class Thermostat(Resource):
    """Get Thermostat"""

    @device_ns.doc("get thermostat by id")
    @device_ns.marshal_with(thermostat, envelope=DeviceType.THERMOSTAT, skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get thermostat by id"""
        my_device = current_app.config["DeviceDAO"].get(id)
        sleep(1)
        if my_device.get("type") != DeviceType.THERMOSTAT:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST,
                f"device {device_id} is not a {DeviceType.THERMOSTAT}",
            )
        return my_device, HTTPStatus.OK

    @device_ns.doc("Update thermostat")
    @device_ns.expect(thermostat)
    @device_ns.marshal_with(thermostat, envelope="thermostat", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update thermostat state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.WATER_HEATER}/<string:device_id>")
class WaterHeater(Resource):
    """Get Water Heater"""

    @device_ns.doc("get water_heater by id")
    @device_ns.marshal_with(water_heater, envelope="water_heater", skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get water_heater by id"""
        my_device = current_app.config["DeviceDAO"].get(id)
        if device.get("type") != DeviceType.WATER_HEATER:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {device_id} is not a water_heater"
            )
        return my_device, HTTPStatus.OK

    @device_ns.doc("Update water_heater")
    @device_ns.expect(water_heater)
    @device_ns.marshal_with(water_heater, envelope="water_heater", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update water_heater state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.WATER_HEATER}/<string:device_id>/usage")
class WaterHeaterPowerUsage(Resource):
    """Get timeseries usage data for Water Heater"""

    @device_ns.doc("get timeseries usage data for Water Heater")
    @device_ns.marshal_list_with(usage_sample, envelope="usage_samples", skip_none=True)
    @jwt_required()
    def get(self, device_id: str):
        """get timeseries usage data for Water Heater"""
        return self.get_timeseries(device_id)

    def get_timeseries(self, device_id: str):
        my_device = current_app.config["DeviceDAO"].get(device_id)
        print(my_device)
        if (
            my_device.get("usage_samples") != []
            and my_device.get("usage_samples") is not None
        ):
            device_samples = list(
                map(
                    lambda sample: {"name": my_device["name"], **sample},
                    my_device["usage_samples"],
                )
            )

            if device_samples is not None and device_samples != []:
                return device_samples, HTTPStatus.OK
        else:
            return None, HTTPStatus.NOT_FOUND


@device_ns.route(f"/{DeviceType.HOME_BATTERY}/<string:device_id>")
class HomeBattery(Resource):
    """Get Home Battery"""

    @device_ns.doc("get home_battery by id")
    @device_ns.marshal_with(home_battery, envelope="home_battery", skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get home_battery by id"""
        my_device = current_app.config["DeviceDAO"].get(device_id)
        if my_device.get("type") != DeviceType.HOME_BATTERY:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {device_id} is not a home_battery"
            )
        return my_device, HTTPStatus.OK

    @device_ns.doc("Update home_battery")
    @device_ns.expect(home_battery)
    @device_ns.marshal_with(home_battery, envelope="home_battery", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update home_battery state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.HOME_BATTERY}/<string:device_id>/update_reserve_limit")
class HomeBatteryReserveLimit(Resource):
    """Update Home Battery Reserve Limit"""

    @device_ns.doc("update home_battery reserve limit")
    @device_ns.expect(home_battery_reserve_limit)
    @device_ns.marshal_with(home_battery, envelope="home_battery", code=HTTPStatus.OK)
    @jwt_required()
    def post(self, device_id):
        """update home_battery reserve limit"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        updated_device = current_app.config[
            "DeviceDAO"
        ].home_battery_reserve_limit_update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return updated_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.HOME_BATTERY}/<string:device_id>/update_charge_rate")
class UpdateHomeBatteryChargeRate(Resource):
    """Update Home Battery Charge Rate"""

    @device_ns.doc("update home_battery charge rate")
    @device_ns.expect(home_battery_charge_rate)
    @device_ns.marshal_with(ev_charger, envelope="home_battery", code=HTTPStatus.OK)
    @jwt_required()
    def post(self, device_id):
        """update home_battery_charger charge rate"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        print("Update battery charge rate", device_ns.payload)
        my_device = current_app.config["DeviceDAO"].home_battery_charge_rate_update(
            device_id, device_ns.payload
        )
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.EV_CHARGER}/<string:device_id>")
class EVCharger(Resource):
    """Get EV Charger"""

    @device_ns.doc("get ev_charger by id")
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get ev_charger by id"""
        my_device = current_app.config["DeviceDAO"].get(device_id)
        if my_device.get("type") != DeviceType.EV_CHARGER:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {device_id} is not a ev_charger"
            )
        return my_device, HTTPStatus.OK

    @device_ns.doc("Update ev_charger")
    @device_ns.expect(ev_charger)
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update ev_charger state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.EV_CHARGER}/<string:device_id>/update_charge_rate")
class UpdateEVChargeRate(Resource):
    """Update EV Charger Charge Rate"""

    @device_ns.doc("update ev_charger charge rate")
    @device_ns.expect(ev_charge_rate)
    @device_ns.marshal_with(ev_charger, envelope="ev_charger", code=HTTPStatus.OK)
    @jwt_required()
    def post(self, device_id):
        """update ev_charger charge rate"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].ev_charge_rate_update(
            device_id, device_ns.payload
        )
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.PV_SYSTEM}/<string:device_id>")
class PVSystem(Resource):
    """Get PV System"""

    @device_ns.doc("get pv_system by id")
    @device_ns.marshal_with(pv_system, envelope="pv_system", skip_none=True)
    @jwt_required()
    def get(self, device_id):
        """get pv_system by id"""
        my_device = current_app.config["DeviceDAO"].get(device_id)
        if my_device.get("type") != DeviceType.PV_SYSTEM:
            device_ns.abort(
                HTTPStatus.BAD_REQUEST, f"device {device_id} is not a pv_system"
            )
        return my_device, HTTPStatus.OK

    @device_ns.doc("Update pv_system")
    @device_ns.expect(pv_system)
    @device_ns.marshal_with(pv_system, envelope="pv_system", code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, device_id):
        """update pv_system state"""
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].update(device_id, device_ns.payload)
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)
        return my_device, HTTPStatus.OK


@device_ns.route(f"/{DeviceType.PV_SYSTEM}/<string:device_id>/generation")
class PVSystemGeneration(Resource):
    """Get timeseries generation data for solar panels"""

    @device_ns.doc("get timeseries generation data for solar panels")
    @device_ns.marshal_list_with(
        generation_sample, envelope="generation_samples", skip_none=True
    )
    @jwt_required()
    def get(self, device_id: str):
        """get timeseries generation data for solar panels"""
        return self.get_timeseries(device_id)

    def shift_generation_sample(self, sample: dict) -> dict:
        now = datetime.now()
        now = now.replace(minute=0, second=0, microsecond=0)
        sample_ts = datetime.fromisoformat(sample["timestamp"])
        new_ts = sample_ts.replace(year=now.year, month=now.month, day=now.day)
        if new_ts.hour > now.hour:
            new_ts = new_ts.replace(day=now.day - 1)

        sample["timestamp"] = new_ts
        return sample

    def get_timeseries(self, device_id: str):
        my_device = current_app.config["DeviceDAO"].get(device_id)
        if (
            my_device.get("generation_samples") != []
            and my_device.get("generation_samples") is not None
        ):
            device_samples = list(
                map(
                    lambda sample: self.shift_generation_sample(sample),
                    my_device["generation_samples"],
                )
            )

            if device_samples is not None and device_samples != []:
                return device_samples, HTTPStatus.OK
        else:
            return None, HTTPStatus.NOT_FOUND


@device_ns.route(f"/{DeviceType.THERMOSTAT}/<string:device_id>/update_setpoint")
class Device(Resource):
    @device_ns.expect(temperature_params)
    @device_ns.doc("Set thermostat temperature")
    @jwt_required()
    def post(self, device_id):
        if device_ns.payload is None:
            return "No payload", HTTPStatus.BAD_REQUEST

        my_device = current_app.config["DeviceDAO"].get(device_id)
        if my_device["type"] != "thermostat":
            return f"Cannot set temperature on {my_device.type}", HTTPStatus.BAD_REQUEST

        updated_device = current_app.config["DeviceDAO"].thermostat_setpoint_update(
            device_id, device_ns.payload
        )
        state["devices"] = current_app.config["DeviceDAO"].get_list()
        save_state(state)

        return updated_device, HTTPStatus.OK
