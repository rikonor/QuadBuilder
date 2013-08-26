from google.appengine.ext import ndb

""" Model classes and utility functions

"""

DEFAULT_MOTOR_GROUP = 'default_motor'
DEFAULT_ESC_GROUP   = 'default_esc'
DEFAULT_PROP_GROUP  = 'default_prop'

def motor_key(motor_group_name=DEFAULT_MOTOR_GROUP):
    """Constructs a Datastore key for a motor_group entity with motor_group_name."""
    return ndb.Key('MotorGroup', motor_group_name)

def esc_key(esc_group_name=DEFAULT_ESC_GROUP):
    """Constructs a Datastore key for a esc_group entity with esc_group_name."""
    return ndb.Key('EscGroup', esc_group_name)

def prop_key(prop_group_name=DEFAULT_PROP_GROUP):
    """Constructs a Datastore key for a prop_group entity with prop_group_name."""
    return ndb.Key('PropGroup', prop_group_name)

class Motor(ndb.Model):
  """Storage for a single Motor and its metadata 

  Properties
    brand:         The brand as a string - ex. 'Turnigy'
    name:          The name as a string  - ex. 'SK-3'
    size:          The size as a string  - ex. '2212'
    kv:            The kV as an integer  - ex. 1100
    weight:        The weight in grams as a float - ex. 49.7
    price:         The price in dollars as a float   - ex. 13.45
  """
  brand = ndb.StringProperty()
  name   = ndb.StringProperty()
  size = ndb.StringProperty(required=True)
  kv = ndb.IntegerProperty(required=True)
  weight = ndb.FloatProperty()
  price = ndb.FloatProperty()

  def toString(self):
    return " ".join([self.brand,
                     self.name,
                     self.size, 
                     str(self.kv)+"kV",
                     str(self.weight)+"gr",
                     "$"+str(self.price)])

class Esc(ndb.Model):
  """Storage for a single ESC and its metadata 

  Properties
    brand:         The brand as a string - ex. 'Suppo'
    name:          The name as a string  - ex. 'HW 25A'
    amp:           The amperage as an integer  - ex. 30
    maxamp:        The maximum amperage as an integer - ex. 40
    weight:        The weight in grams as a float - ex. 49.7
    price:         The price in dollars as a float   - ex. 13.45
  """
  brand = ndb.StringProperty()
  name   = ndb.StringProperty()
  amp = ndb.IntegerProperty(required=True)
  maxamp = ndb.IntegerProperty()
  weight = ndb.FloatProperty()
  price = ndb.FloatProperty()

  def toString(self):
    return " ".join([self.brand,
                     self.name,
                     str(self.amp)+"A", 
                     str(self.maxamp)+"A",
                     str(self.weight)+"gr",
                     "$"+str(self.price)])

class Prop(ndb.Model):
  """Storage for a single Prop and its metadata 

  Properties
    brand:         The brand as a string - ex. 'Suppo'
    name:          The name as a string  - ex. 'HW 25A'
    length:        The length in inches as an integer  - ex. 10
    pitch:         The pitch in inches as a float - ex. 4.5
    weight:        The weight in grams as a float - ex. 49.7
    price:         The price in dollars as a float   - ex. 13.45
  """
  brand = ndb.StringProperty()
  name   = ndb.StringProperty()
  length = ndb.IntegerProperty(required=True)
  pitch = ndb.FloatProperty(required=True)
  weight = ndb.FloatProperty()
  price = ndb.FloatProperty()

  def toString(self):
    return " ".join([self.brand,
                     self.name,
                     str(self.length) + "X" + str(self.pitch),
                     str(self.weight)+"gr",
                     "$"+str(self.price)])
