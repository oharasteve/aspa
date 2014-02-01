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
    forfeits = ndb.IntegerProperty(default=0)
    points = ndb.ComputedProperty(lambda self: 3 * self.wins - 3 * self.forfeits - self.losses / 2.0 + (self.wins + self.forfeits + self.losses) / 1000000.0)
    goal = ndb.ComputedProperty(lambda self: self.highRun * 100.0 / self.highRunTarget if self.highRunTarget and self.highRun else 0.0)
    pct = ndb.ComputedProperty(lambda self: self.wins * 100.0 /(self.wins + self.losses + self.forfeits) if self.wins else 0.0)

    @classmethod
    def getPlayerSummaries(self):
        ret_list = []
        for item in self.query().order(PlayerSummary.season, PlayerSummary.player, PlayerSummary.handicap):
            my_dict = item.to_dict()
            my_dict['player'] = { 'id': my_dict['player'].id(), }
            my_dict['season'] = { 'id': my_dict['season'].id(), }
            ret_list.append(my_dict)
        return ret_list
