from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus

api = Namespace('devices', description='HEMS Operations')

device = api.model('Device', {
    'id': fields.String(readonly=True, description='The Device unique identifier'),
    'name': fields.String(required=True, description='The Device\'s Name'),
    'type': fields.String(required=True, description='The Device\'s Type'),
    'location': fields.String(required=True, description='The Device\'s Location'),
    'status': fields.String(required=True, description='The Device\'s Status'),
    'provisioned': fields.Boolean(required=True, description='The Device\'s Provisioned Status'),
})

class DeviceDAO(object):
    def __init__(self):
        self.devices = []
        
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

DAO = DeviceDAO()

DAO.create({
    "id": "e4d197aa-fa13-4255-b395-63268be12515",
    "name": "Living Room",
    "type": "thermostat",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
})

DAO.create({
    "id": "f8204550-32cc-44aa-bf48-a95a90c1504f",
    "name": "Linda's Charger",
    "type": "car_charger",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
})

DAO.create({
    "id": "8b98e3cf-af15-4ead-8d5e-a2d389723a25",
    "name": "Solar Energy",
    "type": "solar_panels",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
})

DAO.create({
    "id": "a3f67bfe-0b41-4054-889e-fa1d6c5d93d1",
    "name": "Water Heater",
    "type": "water_heater",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
})

DAO.create({
    "id": "052fe39f-5439-4682-beca-b10f2ea00113",
    "name": "Home Battery",
    "type": "home_battery",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
})

@api.route('/')
class DeviceList(Resource):
    '''Shows a list of all devices'''
    @api.doc('list_devices')
    @api.marshal_list_with(device, envelope='devices')
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
    @api.marshal_with(device, envelope='device')
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
