from google.appengine.ext import ndb

class Club(ndb.Model):
    """Models the club locations."""
    name = ndb.StringProperty()
    phone = ndb.StringProperty()
