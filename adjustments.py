from google.appengine.ext import ndb

import players

class Adjustment(ndb.Model):
    """Models a manual handicap update or just a comment."""
    player = ndb.KeyProperty(kind=players.Player)
    date = ndb.DateProperty()
    oldHandicap = ndb.IntegerProperty()
    newHandicap = ndb.IntegerProperty()
    comment = ndb.StringProperty()