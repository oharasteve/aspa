from google.appengine.ext import ndb

import clubs
import players
import seasons

class Match(ndb.Model):
    """Models a match between two players."""
    date = ndb.DateProperty()
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


def match_util(match):
    if not isinstance(match, Match):
        return None

    return {
        'date': match.date,
        'season': match.season,
        'club': match.club,
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
        }
