from json.decoder import JSONDecodeError
from typing import List, Union
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
import json
from pathlib import Path

api = Namespace('devices', description='HEMS Operations')

device = api.model('Device', {
    'id': fields.String(readonly=True, description='The Device unique identifier'),
    'name': fields.String(required=True, description='The Device\'s Name'),
    'type': fields.String(required=True, description='The Device\'s Type'),
    'location': fields.String(required=True, description='The Device\'s Location'),
    'status': fields.String(required=True, description='The Device\'s Status'),
    'provisioned': fields.Boolean(required=True, description='The Device\'s Provisioned Status'),
})


test_device = {
    "id": "e4d197aa-fa13-4255-b395-63268be12515",
    "name": "Living Room",
    "type": "thermostat",
    "location": "Living Room",
    "status": "on",
    "provisioned": True
}

class DeviceDAO(object):
    def __init__(self):
        self.fs_storage_path = Path(__file__).parents[1] / "data" / "device.json"
        self.devices = []
        
        if self.fs_storage_path.exists():
            with open(self.fs_storage_path) as device_data:
                try:
                    self.devices = json.load(device_data)
                except JSONDecodeError:
                    return []
        return self.devices
        return []

        for device in self.read_device_data():
            if device['id'] == device_id:
                return device
        api.abort(HTTPStatus.NOT_FOUND, f"device {device_id} doesn't exist")

        for device in self.read_device_data():
            if device_id == device["id"]:
                return True
        return False
        device = data
        device['id'] = data["id"]
        if  self.device_exists(device["id"]):
            api.abort(HTTPStatus.CONFLICT, f"device {device['id']} already exist")
        devices = self.read_device_data()
        devices.append(device)
        with open(self.fs_storage_path, "w") as device_data:
            json.dump(devices, device_data)
        
        return device

        device = self.get_device_by_id(device_id)
        device.update(data)
        return device

        device = self.get_device_by_id(device_id)
        self.devices.remove(device)  


DAO = DeviceDAO()
DAO.create(test_device)


@api.route('/')
class DeviceList(Resource):
    '''Shows a list of all devices'''
    @api.doc('list_devices')
    @api.marshal_list_with(device)
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
    @api.marshal_with(device)
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
