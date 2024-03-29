from cojourn.api_mock.apis.namespace import hems_ns
from cojourn.api_mock.apis.types import DemandResponseStatus
from flask_restx import fields

hems = hems_ns.model('HEMS', {
    'id': fields.String(readonly=True, description='The HEMS unique identifier'),
    'provisioned': fields.Boolean(required=True, description='The HEMS\'s Provisioned Status'),
    'dr_status': fields.String(
        required=True, 
        description="Demand Response Status",
        enum=[status for status in DemandResponseStatus]
    )
})

hems_der_status = hems_ns.model('HemsDerStatus', {"status": fields.String(required=True, enum=[
                                status for status in DemandResponseStatus], description='The HEMS\'s Der Status')})

hems_jwt = hems_ns.model('HEMS JWT', {'jwt': fields.String(required=True, 
                        description="The JWT used to authenticate to the API")
                        })