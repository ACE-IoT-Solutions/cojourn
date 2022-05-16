from cojourn.api_mock.apis.namespace import device_ns
from cojourn.api_mock.apis.types import (ChargeRate, DemandResponseStatus,
                                 DeviceService, DeviceStatus, DeviceType,
                                 ThermostatMode, Weather)
from flask_restx import fields

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

device_der_status = device_ns.model(
    "DeviceDerStatus",
    {
        "status": fields.String(
            required=True,
            enum=[status for status in DemandResponseStatus],
            description="The Device's DER Status"
        )
    }
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

home_battery_reserve_limit = device_ns.model(
    "HomeBatteryReserveLimit", {"reserve_limit": fields.Integer}
)

home_battery_charge_rate = device_ns.model(
    "HomeBatteryChargeRate",
    {
        "charge_rate": fields.String(
            required=True,
            enum=[val for val in ChargeRate],
            description="Home Battery charge rate",
        )
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


usage_sample = device_ns.model(
    "Usage Sample",
    {
        "name": fields.String(readOnly=True, description="The Device's Name"),
        "timestamp": fields.DateTime(
            readOnly=True, description="Timestamp of the sample"
        ),
        "power_used": fields.Fixed(
            readOnly=True, decimals=2, description="Power Used (wH)"
        ),
    },
)

list_of_usage_samples = device_ns.model(
    "List of Usage Samples",
    {"samples": fields.List(fields.Nested(usage_sample))},
)

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
        "usage_samples": fields.Nested(list_of_usage_samples),
    },
)
