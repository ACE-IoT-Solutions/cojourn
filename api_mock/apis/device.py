import json
from random import sample
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus

import jwt
from state import load_state, save_state

from .types import DemandResponseStatus, DeviceStatus, DeviceService, ThermostatMode, Weather, ChargeRate

api = Namespace('devices', description='Device Operations')

device = api.model('Device', {
    'id': fields.String(required=True, description='The Device unique identifier'),
    'name': fields.String(required=True, description='The Device\'s Name'),
    'type': fields.String(required=True, description='The Device\'s Type'),
    'location': fields.String(required=True, description='The Device\'s Location'),
    'provisioned': fields.Boolean(required=True, description='The Device\'s Provisioned Status'),
    'status': fields.String(required=True, description='The Device\'s Status', enum=[status for status in DeviceStatus]),
    'dr_status': fields.String(required=True, description='Demand Response Status', enum=[status for status in DemandResponseStatus]),

    # Thermostat
    'mode': fields.String(
        required=False, 
        enum=[mode for mode in ThermostatMode],
        description='Thermostat Current Mode'
    ),
    'setpoint': fields.Fixed(decimals=2, required=False, description='Thermostat target temperature (C)'),
    'setpoint_span': fields.Fixed(
        decimals=2, 
        required=False, 
        description='Thermostat setpoint span (C)'
    ),
    'interior_temperature': fields.Fixed(decimals=2, required=False, description='Thermostat Current Temperature (C)'),
    'exterior_temperature': fields.Fixed(decimals=2, required=False, description='Thermostat Exterior Temperature (C)'),
    'exterior_weather': fields.String(
        required=False,
        enum=[weather for weather in Weather],
        description='Weather description'
    )})

generation_sample = api.model('Generation Sample', {
    'name': fields.String(readOnly=True, description='The Device\'s Name'),
    'timestamp': fields.DateTime(readOnly=True, description='Timestamp of the sample'),
    'power_generated': fields.Fixed(readOnly=True, decimals=2, description='Power Generated (wH)'),
    'power_sent_to_grid': fields.Fixed(readonly=True, decimals=2, description='Power Sent to Grid (wH)'),
    })

list_of_generation_samples = api.model('List of Generation Samples', {
    'samples': fields.List(fields.Nested(generation_sample))
    })

# Solar Panels
solar_panels = api.inherit("Solar Panels", device, {
    'label': fields.String(required=False, description='The Device\'s Status (deprecated)', enum=[status for status in DeviceStatus]),
    'power_generated_this_month': fields.Fixed(readOnly=True, decimals=2, description='Power Generated This Month (wH)'),
    'power_sent_to_grid_this_month': fields.Fixed(readOnly=True, decimals=2, description='Power Sent to Grid This Month (wH)'),
    'generation_samples': fields.Nested(list_of_generation_samples)
    })

list_of_solar_panels = api.model('List of Solar Panels', {
    'solar_panels': fields.List(fields.Nested(solar_panels))
    })

# Water Heater

# Home Battery
home_battery = api.inherit("Home Battery", device, {
    "reserve_limit": fields.Fixed(decimals=2, required=False, description='Home Battery Reserve Limit %'),
    'service': fields.String(
        required=False,
        enum=[service for service in DeviceService],
        description='Service description'
    ),
    'charge_percentage': fields.Fixed(decimals=2, required=False, description='The Device\'s Charge Amount %'),
    'charge_rate': fields.String(
        required=False,
        enum=[c for c in ChargeRate],
        description='The Device\'s Charge Rate'
    )})
                           
ev_charger = api.inherit("EV Charger", device, {
    'service': fields.String(
        required=False,
        enum=[service for service in DeviceService],
        description='Service description'
    ),
    'charge_percentage': fields.Fixed(decimals=2, required=False, description='The Device\'s Charge Amount %'),
    'charge_rate': fields.String(
        required=False,
        enum=[c for c in ChargeRate],
        description='The Device\'s Charge Rate'
    )})

# Shared
# 'label': Water Heater, Solar Panels
water_heater = api.inherit("Water Heater", device, {
    'label': fields.String(required=False, description='The Device\'s Status (deprecated)', enum=[status for status in DeviceStatus]),
})
                               

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
        if (device['type'] == 'thermostat'):
            device_mode = ThermostatMode(device['mode'])
            device['setpoint_span'] = self.__thermostat_setpoint_span(device_mode)

        return device

    def __init__(self, devices=[]):
        self.devices = list(map(self.__decorate_device, devices))
        
    def get_list(self):
        return self.devices

    def get(self, id):
        for device in self.devices:
            if device['id'] == id:
                return device
        api.abort(HTTPStatus.NOT_FOUND, f"device {id} doesn't exist")

    def create(self, data):
        device = data
        device['id'] = data["id"]
        self.devices.append(device)
        return device

    def update(self, id, data):
        device = self.get(id)
        device.update(data)
        device.update(self.__decorate_device(device))
        return device

    def delete(self, id):
        device = self.get(id)
        self.devices.remove(device)  

state = load_state()
DAO = DeviceDAO(state.get("devices", []))

@api.route('/')
class DeviceList(Resource):
    '''Shows a list of all devices'''
    @api.doc('list_devices')
    @api.marshal_list_with(device, envelope='devices', skip_none=True)
    @jwt_required()
    def get(self):
        '''List all devices'''
        return DAO.get_list(), HTTPStatus.OK


    @api.doc('create_device')
    @api.expect(device)
    @api.marshal_with(device, envelope='device', code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new device'''
        myDevice = DAO.create(api.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.CREATED


@api.route('/<string:id>')
class Device(Resource):
    '''Get device by id'''
    @api.doc('get device by id')
    @api.marshal_with(device, envelope='device', skip_none=True)
    @jwt_required()
    def get(self, id):
        '''get device by id'''
        return DAO.get(id), HTTPStatus.OK
    
    @api.doc('Update device')
    @api.expect(device)
    @api.marshal_with(device, envelope='device', code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        '''update device state'''
        if (api.payload is None):
            return 'No payload', HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, api.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK
        

@api.route('/solar-panels/generation')
class DeviceType(Resource):
    '''Get timeseries generatio ndata for solar panels'''
    @api.doc('get timeseries generation data for solar panels')
    @api.marshal_list_with(generation_sample, envelope='generation_samples', skip_none=True)
    @jwt_required()
    def get(self):
        '''get timeseries generation data for solar panels'''
        return self.get_timeseries(), HTTPStatus.OK
    
    def get_timeseries(self):
        devices = DAO.get_list()
        solar_panels = (
            [device for device in devices 
             if device['type'].lower() == 'solar_panels' 
             and device.get('generation_samples') is not None
             and device.get('generation_samples') != []]
            )
        samples = []
        
        for device in solar_panels:
            device_samples = list(
                map(
                    lambda sample: {"name": device["name"], **sample}, 
                    device['generation_samples']))
            
            if device_samples is not None and device_samples != []:
                samples += device_samples
        
        return samples
            


temperature_params = api.model('TemperatureParams', {
    'setpoint': fields.Fixed(decimals=2, required=False, description='Thermostat target temperature (C)'),
    'mode': fields.String(
        required=False, 
        enum=[mode for mode in ThermostatMode],
        description='Thermostat Current Mode'
    )
})

@api.route('/<string:id>/temperature')
class Device(Resource):
    @api.expect(temperature_params)
    @api.doc('Set thermostat temperature')
    @jwt_required()
    def post(self, id):
        if (api.payload is None):
            return 'No payload', HTTPStatus.BAD_REQUEST

        device = DAO.get(id)
        if (device['type'] != 'thermostat'):
            return f'Cannot set temperature on {device.type}', HTTPStatus.BAD_REQUEST
        
        updatedDevice = DAO.update(id, api.payload)
        state["devices"] = DAO.get_list()
        save_state(state)
        
        return updatedDevice, HTTPStatus.OK
