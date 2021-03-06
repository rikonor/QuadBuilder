from google.appengine.ext import ndb

""" Model classes and utility functions

"""
# Model Index:
# Part
# General Parts:
# 	Motor
#	ESC
#	Prop
#	FC (Flight Controller) - TODO
#	Frame	- TODO
#	Tx - TODO
#	Rx - TODO
#	Battery - TODO
#	Accessory - TODO
# Spec
# Logistic Stuff:
#	Comment - TODO
#	User	


####################################################################################
# Part class - Abstract ############################################################
####################################################################################
class Part(ndb.Model):
	"""Abstract class for a single part

	Properties:
	  brand:         The brand as a string - ex. 'Turnigy'
	  name:          The name as a string  - ex. 'SK-3'
	  weight:        The weight in grams as a float - ex. 49.7
	  price:         The price in dollars as a float   - ex. 13.45
	"""
	brand = ndb.StringProperty()
	name   = ndb.StringProperty()
	weight = ndb.FloatProperty()
	price = ndb.FloatProperty()
	created = ndb.DateTimeProperty(auto_now_add = True)
####################################################################################
# Motor class ######################################################################
####################################################################################
class Motor(Part):
	"""Storage for a single Motor and its metadata 

	Properties
	size:          The size as a string  - ex. '2212'
	kv:            The kV as an integer  - ex. 1100
	"""
	size = ndb.StringProperty()
	kv = ndb.IntegerProperty()

	def toString(self):
		return " ".join([self.brand,
	                     self.name,
	                     self.size, 
	                     str(self.kv)+"kV",
	                     str(self.weight)+"gr",
	                     "$"+str(self.price)])
####################################################################################
# ESC class ########################################################################
####################################################################################
class Esc(Part):
	"""Storage for a single ESC and its metadata 

	Properties
	amp:           The amperage as an integer  - ex. 30
	maxamp:        The maximum amperage as an integer - ex. 40
	"""
	amp = ndb.IntegerProperty()
	maxamp = ndb.IntegerProperty()

	def toString(self):
		return " ".join([self.brand,
	                     self.name,
	                     str(self.amp)+"A", 
	                     str(self.maxamp)+"A",
	                     str(self.weight)+"gr",
	                     "$"+str(self.price)])
####################################################################################
# Prop class #######################################################################
####################################################################################
class Prop(Part):
	"""Storage for a single Prop and its metadata 

	Properties
	length:        The length in inches as an integer  - ex. 10
	pitch:         The pitch in inches as a float - ex. 4.5
	"""
	length = ndb.IntegerProperty()
	pitch = ndb.FloatProperty()
  
	def toString(self):
		return " ".join([self.brand,
	                     self.name,
	                     str(self.length) + "X" + str(self.pitch),
	                     str(self.weight)+"gr",
	                     "$"+str(self.price)])
####################################################################################
# Spec class #######################################################################
####################################################################################
class Spec(ndb.Model):
	"""This is the model for a build spec
	"""
	motorKey = ndb.KeyProperty(kind=Motor)
	escKey = ndb.KeyProperty(kind=Esc)
	propKey = ndb.KeyProperty(kind=Prop)

	# userKey = ndb.KeyProperty(kind=User)
	userId = ndb.IntegerProperty()
	created = ndb.DateTimeProperty(auto_now_add = True)

	def toString(self):
		return "<br>".join([self.motorKey.get().toString(),
	                     self.escKey.get().toString(),
	                     self.propKey.get().toString(),
	                     ])
####################################################################################
# User class #######################################################################
####################################################################################
class User(ndb.Model):
	"""This is the model for a single user
	"""
	# Signup/Login data
	name = ndb.StringProperty(required = True)
	pw_hash = ndb.StringProperty(required = True)
	email   = ndb.StringProperty()
	created = ndb.DateTimeProperty(auto_now_add = True)
	# User information
	about = ndb.TextProperty()
	specsKey = ndb.KeyProperty(kind=Spec, repeated=True)

	def toString(self):
    # return self.motorKey
		return " ".join([self.name,
	                     ])
####################################################################################
