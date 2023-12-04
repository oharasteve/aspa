from google.appengine.ext import ndb

import logging

#
# Current statistics for each player, per season. These do not have history.
# They only have the current values for handicaps, etc.
#
# When modifing stats you must use one of the accessor functions (addMatch/removeMatch)
# as they are used to keep the lifetime stats structure in sync with the season
# currently being run. It is still correct to use the Stat class to query a record for
# display but NOT for updating any of the contained information.
#
# Creating a new session causes no issues but creating a new player needs to create the
# lifetime record for them as well.
#

import players
import seasons

def getHighRunTarget(handicap):
  if handicap < 400 or handicap >= 850:
    return 0

  highRunAdjust = 0.8; # Per Tan targets are too high
  # This is a lookup table for calculating high run target,
  # given a player's handicap. It is a piecewise linear function,
  # interpolating between the points
  highRuns = [
    [350, 16],
    [400, 18],
    [450, 20],
    [500, 22],
    [550, 26],
    [600, 32],
    [650, 44],
    [700, 58],
    [725, 72],
    [750, 86],
    [775, 100],
    [800, 114],
    [825, 128],
    [850, 144]
  ];

  for i in range(len(highRuns)):
    if handicap < highRuns[i][0]:
      break;

  prev_handicap = highRuns[i-1][0];
  prev_target = highRuns[i-1][1] * highRunAdjust;
  scale = (1.0*highRuns[i][0] - prev_handicap) / (highRuns[i][1] * highRunAdjust - prev_target);
  return int((prev_target + (handicap - prev_handicap) / scale) + 0.5)

def addMatch(season, player, win, hcap, score, hrun):

   Stats = PlayerSummary.query(
       ndb.AND(PlayerSummary.player == player, PlayerSummary.season == season)).fetch(1)[0]

   # Update win / loss totals
   hcapAdj = 0
   if win == 1:
      hcapAdj = 3
   elif win == 0:
      hcapAdj = -3
   else:
      hcapAdj = -3
   if Stats.wins + Stats.losses < 30 or season.id() == 'lifetime':
       if win == 1:
          Stats.wins = Stats.wins + 1
       elif win == 0:
          Stats.losses = Stats.losses + 1
       else:
          Stats.forfeits = Stats.forfeits + 1

   if season.id() != 'lifetime':
       # Update handicaps
       if hrun >= Stats.highRunTarget/2:
           Stats.HighRunCount += 1
       _player = player.get()
       _player.handicap = _player.handicap + hcapAdj
       _player.put()
       Stats.handicap = _player.handicap
       Stats.highRunTarget = getHighRunTarget(_player.handicap)

   # Update high runs
   if hrun > Stats.highRun:
       Stats.highRun = hrun

   if hrun > 0:
       Stats.highRuns.append(hrun)

   Stats.put()

def removeMatch(season, player, win, hrun):

   Stats = PlayerSummary.query(
       ndb.AND(PlayerSummary.player == player, PlayerSummary.season == season)).fetch(1)[0]

   # Update win / loss totals
   hcapAdj = 0
   if win == 1:
      Stats.wins = Stats.wins - 1
      hcapAdj = 3
   elif win == 0:
      Stats.losses = Stats.losses - 1
      hcapAdj = -3
   else:
      Stats.forfeits = Stats.forfeits - 1
      hcapAdj = -3

   # Update handicaps
   _player = player.get()
   _player.handicap = _player.handicap - hcapAdj
   _player.put()

   Stats.highRunTarget = getHighRunTarget(_player.handicap)
   if hrun >= Stats.highRunTarget/2:
       Stats.HighRunCount -= 1

   Stats.highRuns.remove(hrun)
   """
   TODO:
   We should scan session/all history for next lower IF hrun == highRun

   # Update high runs
   if hrun > Stats.highRun:
       Stats.highRun = hrun
   """

   Stats.put()


class PlayerSummary(ndb.Model):
    """Models a players statistics for the season."""
    player = ndb.KeyProperty(kind=players.Player)
    season = ndb.KeyProperty(kind=seasons.Season)
    handicap = ndb.IntegerProperty()
    highRunTarget = ndb.FloatProperty(default=999)
    highRun = ndb.IntegerProperty()
    highRuns = ndb.IntegerProperty(repeated=True)
    highRunCount = ndb.IntegerProperty(default=0)
    wins = ndb.IntegerProperty()
    losses = ndb.IntegerProperty()
    forfeits = ndb.IntegerProperty(default=0)
    points = ndb.ComputedProperty(lambda self: 3 * self.wins - 3 * self.forfeits - self.losses / 2.0 + (self.wins + self.forfeits + self.losses) / 1000000.0)
    goal = ndb.ComputedProperty(lambda self: self.highRun * 100.0 / self.highRunTarget if self.highRunTarget else 0.0)
    pct = ndb.ComputedProperty(lambda self: self.wins * 100.0 / (self.wins + self.losses + self.forfeits) if self.wins else 0.0)

    @classmethod
    def getPlayerSummaries(self, ssn):
        ret_list = []
        for item in self.query(PlayerSummary.season == ssn.key).order(PlayerSummary.player):
            my_dict = item.to_dict()
            player = players.Player.get_by_id(item.player.id())
            my_dict['player'] = {
                'id': item.player.id(),
                'firstName': player.firstName,
                'lastName': player.lastName,
                }
            ret_list.append(my_dict)
        return ret_list

    @classmethod
    def getPlayers(self, ssn):
        playerdict = {}
        ret_list = []
        logging.info("players for "+ssn.key.id()+" for club "+ssn.club.id())
        for item in self.query(PlayerSummary.season == ssn.key).order(PlayerSummary.player):
            if item.player.id() in playerdict:
               continue
            player = players.Player.get_by_id(item.player.id())
            playerdict[item.player.id()] = item.player.get()
        for player in playerdict:
            my_dict = playerdict[player].to_dict()
            my_dict['id'] = playerdict[player].key.id()
            ret_list.append(my_dict)
        logging.info(ret_list)
        return ret_list
