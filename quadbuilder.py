import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from models import *
from AddHandlers import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):

    def get(self):
        # Get the motors from the datastore
        motor_group_name = self.request.get('motor_group_name', DEFAULT_MOTOR_GROUP)
        motors_query = Motor.query(ancestor=motor_key(motor_group_name))
        motors = motors_query.fetch(10)
        # Get the escs from the datastore
        esc_group_name = self.request.get('esc_group_name', DEFAULT_ESC_GROUP)
        escs_query = Esc.query(ancestor=esc_key(esc_group_name))
        escs = escs_query.fetch(10)
        # Get the props from the datastore
        prop_group_name = self.request.get('prop_group_name', DEFAULT_PROP_GROUP)
        props_query = Prop.query(ancestor=prop_key(prop_group_name))
        props = props_query.fetch(10)
        # Put parts in dictionary
        template_values = {
            'motors': motors,
            'escs': escs,
            'props': props,
        }
        # Generate the page, pass motors and escs.
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class AddHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render())

class PermalinkHandler(webapp2.RequestHandler):

    def get(self, kind, entry_id):

        part = None
        if kind == 'Motor':
            part = Motor.get_by_id(int(entry_id), parent=motor_key())
        elif kind == 'ESC':
            part = Esc.get_by_id(int(entry_id), parent=esc_key())
        elif kind == 'Prop':
            part = Prop.get_by_id(int(entry_id), parent=prop_key())
        
        if part:
            self.response.write(part.toString())
        else:
            self.response.write("No such part.")        

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Add', AddHandler),
    ('/AddMotor', AddMotor),
    ('/AddEsc', AddEsc),
    ('/AddProp', AddProp),
    ('/(Motor|ESC|Prop)/(\d+)', PermalinkHandler),
], debug=True)