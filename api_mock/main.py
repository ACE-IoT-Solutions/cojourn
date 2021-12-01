from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='0.0.1', title='Cojourn API Mock',
    description='API Mock for testing Cojourn',
)

users_ns = api.namespace('users', description='User Operations')
hems_ns = api.namespace('hems', description='HEMS Operations')
devices_ns = api.namespace('devices', description='HEMS Operations')

user = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='The User\'s First Name'),
    'last_name': fields.String(required=True, description='The User\'s Last Name'),
    'birthdate': fields.Date(required=True, description='The User\'s Birthdate'),
    'email': fields.String(required=True, description='The User\'s Email'),
})

hems = api.model('HEMS', {
    'id': fields.String(readonly=True, description='The HEMS unique identifier'),
    'provisioned': fields.Boolean(required=True, description='The HEMS\'s Provisioned Status'),
})

device = api.model('Device', {
    'id': fields.String(readonly=True, description='The Device unique identifier'),
    'name': fields.String(required=True, description='The Device\'s Name'),
    'type': fields.String(required=True, description='The Device\'s Type'),
    'location': fields.String(required=True, description='The Device\'s Location'),
    'status': fields.String(required=True, description='The Device\'s Status'),
    'provisioned': fields.Boolean(required=True, description='The Device\'s Provisioned Status'),
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@hems_ns.route('/')
class HEMS(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @hems_ns.doc('list_hems')
    @hems_ns.marshal_list_with(hems)
    def get(self):
        '''List all tasks'''


    @hems_ns.doc('create_todo')
    @hems_ns.expect(hems)
    @hems_ns.marshal_with(hems, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201

@devices_ns.route('/')
class Device(Resource):
    '''Shows a list of all devices'''
    @devices_ns.doc('list_devices')
    @devices_ns.marshal_list_with(device)
    def get(self):
        '''List all devices'''


    @devices_ns.doc('create_device')
    @devices_ns.expect(device)
    @devices_ns.marshal_with(device, code=201)
    def post(self):
        '''Create a new device'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)