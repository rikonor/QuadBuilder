"""This module contains different handlers for adding items to the datastore 
"""

from google.appengine.ext import ndb
from models import *
import quadbuilder

import webapp2
import time

###############################################################
# AddMotor handler ############################################
###############################################################
class AddMotor(webapp2.RequestHandler):

    def post(self):
        # Create
        motor = Motor()
        # Populate
        motor.brand  =  self.request.get('motorBrand')
        motor.name   =  self.request.get('motorName')
        motor.size   =  self.request.get('motorSize')
        motor.kv     =  int(self.request.get('motorKv'))
        motor.weight =  float(self.request.get('motorWeight'))
        motor.price  =  float(self.request.get('motorPrice'))
        # Insert
        motor.put()
        # Sleep is due to DB consistency issues
        time.sleep(0.1)

        self.redirect('/')
###############################################################
# AddESC handler ##############################################
###############################################################
class AddEsc(webapp2.RequestHandler):

    def post(self):
        # Create
        esc = Esc()
        # Populate
        esc.brand   =  self.request.get('escBrand')
        esc.name    =  self.request.get('escName')
        esc.amp     =  int(self.request.get('escAmp'))
        esc.maxamp  =  int(self.request.get('escMaxAmp'))
        esc.weight  =  float(self.request.get('escWeight'))
        esc.price   =  float(self.request.get('escPrice'))
        # Insert
        esc.put()
        # Sleep is due to DB consistency issues
        time.sleep(0.1)

        self.redirect('/')
###############################################################
# AddProp handler #############################################
###############################################################
class AddProp(webapp2.RequestHandler):

    def post(self):
        # Create
        prop = Prop()
        # Populate
        prop.brand   =  self.request.get('propBrand')
        prop.name    =  self.request.get('propName')
        prop.length  =  int(self.request.get('propLength'))
        prop.pitch   =  float(self.request.get('propPitch'))
        prop.weight  =  float(self.request.get('propWeight'))
        prop.price   =  float(self.request.get('propPrice'))
        # Insert
        prop.put()
        # Sleep is due to DB consistency issues
        time.sleep(0.1)

        self.redirect('/')
###############################################################
# AddSpec handler #############################################
###############################################################
class AddSpec(webapp2.RequestHandler):

    def post(self):

        # Collect parts from datastore according to their id's.
        motorId = self.request.get('motorId')
        motor   = Motor.get_by_id(int(motorId))        
        escId = self.request.get('escId')
        esc   = Esc.get_by_id(int(escId))
        propId = self.request.get('propId')
        prop   = Prop.get_by_id(int(propId))

        # Create Spec object, populate and save it.
        spec = Spec()
        # Populate
        spec.motorKey = motor.key
        spec.escKey   = esc.key
        spec.propKey  = prop.key

        # Find User in DB. (Authenticate (from quadbuilder.py))
        user_id = quadbuilder.Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))

        # Insert (and attach Spec to User)
        if user:
            spec.userId = user.key.id()
        specKey = spec.put()
        if user:
            user.specsKey.append(specKey)
            user.put()
        
        # Sleep is due to DB consistency issues
        time.sleep(0.1)

        self.redirect('/')
###############################################################
