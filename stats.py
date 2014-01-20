from google.appengine.ext import ndb

import players
import seasons

class PlayerSummary(ndb.Model):
  """Models a players statistics for the season."""
  player = ndb.KeyProperty(kind=players.Player)
  season = ndb.KeyProperty(kind=seasons.Season)
  handicap = ndb.IntegerProperty()
  highRunTarget = ndb.FloatProperty()
  highRun = ndb.IntegerProperty()
  wins = ndb.IntegerProperty()
  losses = ndb.IntegerProperty()

def insertJavascript(response):
  response.write('  function findHandicap(key) {\n')
  for stat in PlayerSummary.query():
    response.write('    if (key == "{0}") return {1};\n'.format(stat.player.id(), stat.handicap))
  response.write('    return 0;\n')
  response.write('  }\n')
