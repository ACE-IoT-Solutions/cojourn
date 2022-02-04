from flask_restx import Namespace


user_ns = Namespace('user', description='User Operations')
device_ns = Namespace("devices", description="Device Operations")
auth_ns = Namespace('auth', description='Authentication Operations')
home_ns = Namespace('home', description='Home Operations')
hems_ns = Namespace('hems', description='HEMS Operations')
