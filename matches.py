from google.appengine.ext import ndb

import clubs
import players
import seasons

class Match(ndb.Model):
    """Models a match between two players."""
    date = ndb.DateProperty()
    season = ndb.KeyProperty(kind=seasons.Season)
    club = ndb.KeyProperty(kind=clubs.Club)

    playerW = ndb.KeyProperty(kind=players.Player)
    handicapW = ndb.IntegerProperty()
    scoreW = ndb.IntegerProperty()
    targetW = ndb.IntegerProperty()
    highRunW = ndb.IntegerProperty()

    playerL = ndb.KeyProperty(kind=players.Player)
    handicapL = ndb.IntegerProperty()
    scoreL = ndb.IntegerProperty()
    targetL = ndb.IntegerProperty()
    highRunL = ndb.IntegerProperty()
