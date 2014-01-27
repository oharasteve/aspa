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
  pct = ndb.FloatProperty(default=0.0)
  points = ndb.ComputedProperty(lambda self: 3 * self.wins - self.losses / 2.0 + (self.wins + self.losses) / 1000000.0)
  goal = ndb.ComputedProperty(lambda self: self.highRun * 100.0 / self.highRunTarget if self.highRunTarget and self.highRun else 0.0)
  pct = ndb.ComputedProperty(lambda self: self.wins * 100.0 /(self.wins + self.losses) if self.wins else 0.0)


def insertJavascript(response):
  response.write('  function findHandicap(key) {\n')
  for stat in PlayerSummary.query():
    response.write('    if (key == "{0}") return {1};\n'.format(stat.player.id(), stat.handicap))
  response.write('    return 0;\n')
  response.write('  }\n')
