from google.appengine.ext import ndb

import base_handler
import cgi
import matches
import players
import seasons
import stats
import webapp2

TEMPLATE = 'html/details.html'


class DetailsHandler(base_handler.BaseHandler):
    def get(self):
        season = seasons.Season.get_by_id(self.request.get('Season'))
        player = players.Player.get_by_id(self.request.get('Player'))

        # Show the webpage
        context = Details().get_context(season, player)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/details/', DetailsHandler)],
    debug=True,
    config=base_handler.CONFIG)

class Details():
    def get_match_details(self, season, player):
        entries = []
        seq = 0
        season_matches = matches.Match.query( ndb.AND( ndb.OR(
            matches.Match.playerW == player.key, matches.Match.playerL ==
            player.key), stats.PlayerSummary.season == season.key
            )).order(matches.Match.date)
        for match in season_matches:
            seq += 1
            match_data = matches.match_util(match)
            if player.key == match_data['winner']['player']:
                participant = match_data['winner']
                opponent = match_data['loser']
                result = 'Won'
            else:
                participant = match_data['loser']
                opponent = match_data['winner']
                result = 'Lost'

            participant['player_obj'] = players.Player.get_by_id(
                    participant['player'].id())
            opponent['player_obj'] = players.Player.get_by_id(
                    opponent['player'].id())
            entry = {
                    'entry_index': seq,
                    'results_pdf_url': '/results/LSB_{0}.pdf'.format(
                        match.date),
                    'date': match.date,
                    'result': result,
                    'player': participant,
                    'opponent': opponent,
                    'opponent_details_page_url':
                    '/details/?Season={0}&Player={1}'.format(
                        cgi.escape(season.key.id()),
                        cgi.escape(opponent['player'].id())),
                    }
            entries.append(entry)
        return entries

    def get_summary(self, season, player):
        stat = stats.PlayerSummary.query( ndb.AND(
            stats.PlayerSummary.player == player.key,
            stats.PlayerSummary.season == season.key)
            ).fetch(1)[0]
        return stat


    def get_context(self, season, player):
        match_details = self.get_match_details(season, player)
        summary = self.get_summary(season, player)
        context = {
                'season': season,
                'match_details': match_details,
                'player': player,
                'summary': summary,
                }
        return context
