from google.appengine.ext import ndb

#
# When the League Manager wants to manually adjust a players handicap, they
# will create another row in this table. It can probably be used just to keep
# comments as well, without changing the handicap.
#

import players
import seasons

class Adjustment(ndb.Model):
    """Models a manual handicap update or just a comment."""
    player = ndb.KeyProperty(kind=players.Player)
    season = ndb.KeyProperty(kind=seasons.Season)
    date = ndb.DateProperty()
    oldHandicap = ndb.IntegerProperty()
    newHandicap = ndb.IntegerProperty()
    comment = ndb.StringProperty()