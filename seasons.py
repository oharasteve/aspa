from google.appengine.ext import ndb

class Season(ndb.Model):
    """Models a playing season."""
    name = ndb.StringProperty()
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
