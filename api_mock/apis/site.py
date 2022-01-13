from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import fields, Namespace, Resource
from http import HTTPStatus
from state import load_state, save_state
from operator import itemgetter

api = Namespace('home', description='Home Operations')
lpc_config = api.model("Lpc Config", {
        "name": fields.String(description="LPC name"),
        "status_communication": fields.Boolean(description="Whether the home is communicating"),
        "technical_contact": fields.String(description="Technical contact phone/email/phone and email"),
        "technical_phone": fields.String(description="Technical contact phone number"),
        "technical_email": fields.String(description="Technical contact email"),
        })

site = api.model('Site', {
    'id': fields.String(readonly=True, description='The Site unique identifier'),
    "lpc_config": fields.Nested(lpc_config)
})

class SiteDAO(object):
    def __init__(self, sites=[]):
        self.sites = sites
        self.curr_id = 0 if sites == [] else sorted(sites, key=itemgetter("id"))[-1]["id"]
        
    def get_list(self):
        return self.sites

    def get(self, id):
        for site in self.sites:
            if site['id'] == id:
                return site
        api.abort(HTTPStatus.NOT_FOUND, f"site {id} doesn't exist")

    def create(self, data):
        site = data
        site['id'] = self.curr_id
        print(f"{self.curr_id=}")
        self.curr_id += 1
        self.sites.append(site)
        return site

    def update(self, id, data):
        site = self.get(id)
        site.update(data)
        return site

    def delete(self, id):
        site = self.get(id)
        self.sites.remove(site)  

state = load_state()
DAO = SiteDAO(state.get("sites", []))

@api.route('/')
class DeviceList(Resource):
    '''Shows a list of all sites'''
    @api.doc('list_sites')
    @api.marshal_list_with(site, envelope='sites', skip_none=True)
    @jwt_required()
    def get(self):
        '''List all sites'''
        return DAO.get_list(), HTTPStatus.OK


    @api.doc('create_site')
    @api.expect(site)
    @api.marshal_with(site, envelope='site', code=HTTPStatus.CREATED)
    @jwt_required()
    def post(self):
        '''Create a new site'''
        myDevice = DAO.create(api.payload)
        state["sites"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.CREATED


@api.route('/<int:id>')
class Site(Resource):
    '''Get site by id'''
    @api.doc('get site by id')
    @api.marshal_with(site, envelope='site', skip_none=True)
    @jwt_required()
    def get(self, id):
        '''get site by id'''
        return DAO.get(id), HTTPStatus.OK
    
    @api.doc('update_device')
    @api.expect(site)
    @api.marshal_with(site, envelope='site', code=HTTPStatus.OK)
    @jwt_required()
    def patch(self, id):
        '''update site state'''
        if (api.payload is None):
            return 'No payload', HTTPStatus.BAD_REQUEST

        myDevice = DAO.update(id, api.payload)
        state["sites"] = DAO.get_list()
        save_state(state)
        return myDevice, HTTPStatus.OK
