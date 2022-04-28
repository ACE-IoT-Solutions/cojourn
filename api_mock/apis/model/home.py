from api_mock.apis.namespace import home_ns
from flask_restx import fields

status_message = home_ns.model('StatusMessage', {
    'title': fields.String(required=True, description='The title of the message'),
    'message': fields.String(required=True, description='The message')
})
lpc_config = home_ns.model("LPC Config", {
    "name": fields.String(description="LPC name"),
    "status_communication": fields.Boolean(description="Whether the LPC can send custom status messages"),
    "technical_contact": fields.String(description="Technical contact phone/email/phone and email"),
    "technical_phone": fields.String(description="Technical contact phone number"),
    "technical_email": fields.String(description="Technical contact email"),
    "default_event_message": fields.Nested(status_message),
    "current_event_message": fields.Nested(status_message),
})

home = home_ns.model('Home', {
    'id': fields.String(readonly=True, description='The Home unique identifier'),
    "lpc_config": fields.Nested(lpc_config)
})
