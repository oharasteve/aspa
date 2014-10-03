from google.appengine.ext import ndb

#
# One row per match. Each match has two players, a winner and a loser.
# The match takes place at a club, in a season. This data is only for
# that one event, there are no statistics updated here.
#

import clubs
import players
import seasons

class Match(ndb.Model):
    """Models a match between two players."""
    date = ndb.DateProperty()
    seq = ndb.IntegerProperty()
    season = ndb.KeyProperty(kind=seasons.Season)
    club = ndb.KeyProperty(kind=clubs.Club)
    forfeited = ndb.BooleanProperty(default=False)

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
    
    video1 = ndb.StringProperty()
    video2 = ndb.StringProperty()


def match_util(match):
    if not isinstance(match, Match):
        return None

    return {
        'date': match.date,
        'seq': match.seq,
        'season': match.season,
        'club': match.club,
        'forfeited': match.forfeited,
        'winner': {
            'player': match.playerW,
            'player_id': match.playerW.id(),
            'handicap': match.handicapW,
            'score': match.scoreW,
            'target': match.targetW,
            'highRun': match.highRunW,
        },
        'loser': {
            'player': match.playerL,
            'player_id': match.playerL.id(),
            'handicap': match.handicapL,
            'score': match.scoreL,
            'target': match.targetL,
            'highRun': match.highRunL,
        },
        'video1': match.video1,
        'video2': match.video2,
    }
