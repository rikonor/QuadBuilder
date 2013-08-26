"""This module contains different handlers for adding items to the datastore 
"""

from google.appengine.ext import ndb
from models import *

import webapp2

class AddMotor(webapp2.RequestHandler):

    def post(self):
        motor_group_name = self.request.get('motor_group_name',
                                            DEFAULT_MOTOR_GROUP)
        motor = Motor(parent=motor_key(motor_group_name))

        motor.brand  =  self.request.get('motorBrand')
        motor.name   =  self.request.get('motorName')
        motor.size   =  self.request.get('motorSize')
        motor.kv     =  int(self.request.get('motorKv'))
        motor.weight =  float(self.request.get('motorWeight'))
        motor.price  =  float(self.request.get('motorPrice'))

        motor.put()

        self.redirect('/')

class AddEsc(webapp2.RequestHandler):

    def post(self):
        esc_group_name = self.request.get('esc_group_name',
                                            DEFAULT_ESC_GROUP)
        esc = Esc(parent=esc_key(esc_group_name))

        esc.brand   =  self.request.get('escBrand')
        esc.name    =  self.request.get('escName')
        esc.amp     =  int(self.request.get('escAmp'))
        esc.maxamp  =  int(self.request.get('escMaxAmp'))
        esc.weight  =  float(self.request.get('escWeight'))
        esc.price   =  float(self.request.get('escPrice'))

        esc.put()

        self.redirect('/')

class AddProp(webapp2.RequestHandler):

    def post(self):
        prop_group_name = self.request.get('prop_group_name',
                                            DEFAULT_PROP_GROUP)
        prop = Prop(parent=prop_key(prop_group_name))

        prop.brand   =  self.request.get('propBrand')
        prop.name    =  self.request.get('propName')
        prop.length  =  int(self.request.get('propLength'))
        prop.pitch   =  float(self.request.get('propPitch'))
        prop.weight  =  float(self.request.get('propWeight'))
        prop.price   =  float(self.request.get('propPrice'))

        prop.put()

        self.redirect('/')