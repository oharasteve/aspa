from google.appengine.ext import ndb

import base_handler
import cgi
import webapp2

from data import matches
from data import players
from data import stats

TEMPLATE = 'html/charts.html'

class ChartsHandler(base_handler.BaseHandler):
    def get(self):
        player = players.Player.get_by_id(self.request.get('Player'))

        # Show the webpage
        context = Charts().get_context(player)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/charts/', ChartsHandler)],
    debug=True,
    config=base_handler.CONFIG)

class Charts():
    def get_match_details(self, player):
        entries = []
        seq = 0
        season_matches = matches.Match.query( ndb.OR(
            matches.Match.playerW == player.key, matches.Match.playerL ==
            player.key))
        for match in season_matches:
            seq += 1
            match_data = matches.match_util(match)
            if player.key == match_data['winner']['player']:
                participant = match_data['winner']
                opponent = match_data['loser']
                result = 'Won'
                win_mgn = opponent['target'] - opponent['score']
                lose_mgn = ''
            else:
                participant = match_data['loser']
                opponent = match_data['winner']
                lose_mgn = participant['target'] - participant['score']
                win_mgn = ''
                if match_data['forfeited']:
                    result = 'Forfeit'
                else:
                    result = 'Lost'

            participant['player_obj'] = players.Player.get_by_id(
                    participant['player'].id())
            opponent['player_obj'] = players.Player.get_by_id(
                    opponent['player'].id())
            entry = {
                    'entry_index': seq,
                    'results_pdf_url': '/weekly/?Y=%d&M=%d&D=%d' %
                        (match.date.year, match.date.month, match.date.day),
                    'date': match.date,
                    'result': result,
                    'player': participant,
                    'opponent': opponent,
                    'win_mgn': win_mgn,
                    'lose_mgn': lose_mgn,
                    'video1': match.video1,
                    'video2': match.video2,
            }
            entries.append(entry)
        return entries

    def get_summary(self, player):
        stat = stats.PlayerSummary.query( 
            stats.PlayerSummary.player == player.key
            ).fetch(1)[0]
        return stat


    def get_context(self, player):
        match_details = self.get_match_details(player)
        summary = self.get_summary(player)
        context = {
                'match_details': match_details,
                'player': player,
                'summary': summary,
                }
        return context
