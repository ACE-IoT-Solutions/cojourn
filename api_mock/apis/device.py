from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
from state import load_state

api = Namespace('devices', description='HEMS Operations')

device = api.model('Device', {
    'id': fields.String(readonly=True, description='The Device unique identifier'),
    'name': fields.String(required=True, description='The Device\'s Name'),
    'type': fields.String(required=True, description='The Device\'s Type'),
    'location': fields.String(required=True, description='The Device\'s Location'),
    'status': fields.String(required=True, description='The Device\'s Status'),
    'provisioned': fields.Boolean(required=True, description='The Device\'s Provisioned Status'),

    # Thermostat
    'current_temperature': fields.Fixed(decimals=2, required=False, description='Thermostat Current Temperature (C)'),
    'mode': fields.String(required=False, description='Thermostat Current Mode (auto, heat, cool, eco, off)'),

    # Car Charger
    'charge_rate': fields.String(required=False, description='Car Charger Charge Rate (idle, low, medium, high)'),

    # Solar Panels
    'power_generated_today': fields.Fixed(decimals=2, required=False, description='Solar Panels Power Generated Today (wH)'),

    # Water Heater
    'label': fields.String(required=False, description='The Device\'s Status Label (active, inactive)'),

    # Home Battery
    'charge_percentage': fields.Fixed(decimals=2, required=False, description='Home Battery % Charged')
})

class DeviceDAO(object):
    def __init__(self, devices):
        self.devices = devices
        
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
        return device

    def delete(self, id):
        device = self.get(id)
        self.devices.remove(device)  

state = load_state()
DAO = DeviceDAO(state['devices'])

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
    @api.marshal_with(device, code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new device'''
        api.pa
        return DAO.create(api.payload), HTTPStatus.CREATED


@api.route('/<string:id>')
class Device(Resource):
    '''Get device by id'''
    @api.doc('get device by id')
    @api.marshal_with(device, envelope='device', skip_none=True)
    @jwt_required()
    def get(self, id):
        '''get device by id'''
        return DAO.get(id), HTTPStatus.OK


    @api.doc('create_device')
    @api.expect(device)
    @api.marshal_with(device, code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new device'''
        return DAO.create(api.payload), HTTPStatus.CREATED
    
    
    @api.doc('update_device')
    @api.expect(device)
    @api.marshal_with(device, code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        '''update device state'''
        return DAO.update(api.payload), HTTPStatus.OK
