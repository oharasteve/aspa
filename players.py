from google.appengine.ext import ndb

class Player(ndb.Model):
  """Models a player."""
  firstName = ndb.StringProperty()
  lastName = ndb.StringProperty()
  phone = ndb.StringProperty()

