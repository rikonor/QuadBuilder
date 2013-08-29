from google.appengine.ext import ndb

""" Model classes and utility functions

"""

DEFAULT_MOTOR_GROUP = 'default_motor'
DEFAULT_ESC_GROUP   = 'default_esc'
DEFAULT_PROP_GROUP  = 'default_prop'
DEFAULT_SPEC_GROUP  = 'default_spec'

def motor_key(motor_group_name=DEFAULT_MOTOR_GROUP):
    """Constructs a Datastore key for a motor_group entity with motor_group_name."""
    return ndb.Key('MotorGroup', motor_group_name)

def esc_key(esc_group_name=DEFAULT_ESC_GROUP):
    """Constructs a Datastore key for a esc_group entity with esc_group_name."""
    return ndb.Key('EscGroup', esc_group_name)

def prop_key(prop_group_name=DEFAULT_PROP_GROUP):
    """Constructs a Datastore key for a prop_group entity with prop_group_name."""
    return ndb.Key('PropGroup', prop_group_name)

def spec_key(spec_group_name=DEFAULT_SPEC_GROUP):
    """Constructs a Datastore key for a spec_group entity with spec_group_name."""
    return ndb.Key('SpecGroup', spec_group_name)


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

class Spec(ndb.Model):
  """This is the model for a build spec
  """
  motorKey = ndb.KeyProperty(kind=Motor)
  escKey = ndb.KeyProperty(kind=Esc)
  propKey = ndb.KeyProperty(kind=Prop)

  def toString(self):
    # return self.motorKey
    return " ".join([self.motorKey.get().toString(),
                     self.escKey.get().toString(),
                     self.propKey.get().toString(),
                     ])