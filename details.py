from google.appengine.ext import ndb
import cgi
import webapp2
import os

import jinja2
import matches
import players
import seasons
import stats


def datetimeformat(value, my_format='%b %d, %Y'):
    return value.strftime(my_format)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['datetimeformat'] = datetimeformat


class DetailHandler(webapp2.RequestHandler):
    def get(self):
        season = seasons.Season.get_by_id(self.request.get('Season'))
        player = players.Player.get_by_id(self.request.get('Player'))

        # Show the webpage
        d = Details()
        d.showPage(JINJA_ENVIRONMENT, self.response, season, player)

app = webapp2.WSGIApplication([ ('/details/', DetailHandler) ], debug=True)

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
                protagonist = match_data['winner']
                opponent = match_data['loser']
                result = 'Won'
            else:
                protagonist = match_data['loser']
                opponent = match_data['winner']
                result = 'Lost'

            protagonist['player_obj'] = players.Player.get_by_id(protagonist['player'].id())
            opponent['player_obj'] = players.Player.get_by_id(opponent['player'].id())
            entry = {
                    'entry_index': seq,
                    'alternate_class': 'even' if seq % 2 == 0 else 'odd',
                    'results_pdf_url': '/results/LSB_{0}.pdf'.format(
                        match.date),
                    'date': match.date,
                    'result': result,
                    'player': protagonist,
                    'opponent': opponent,
                    'opponent_details_page_url':
                    'details/?Season={0}&Player={1}'.format(
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


    def get_template_values(self, season, player):
        match_details = self.get_match_details(season, player)
        summary = self.get_summary(season, player)
        template_values = {
                'season': season,
                'match_details': match_details,
                'player': player,
                'summary': summary,
                'site_admin': {
                    'email': 'site_admin_email',
                    'name': 'site_admin_name',
                    },
                'league_manager': {
                    'email': 'league_manager_email',
                    'name': 'league_manager_name',
                    },
                'page': {
                    'last_updated_date': '2014-01-27 12:00:00',
                    },
                }
        return template_values

    def showPage(self, jinja_environment, response, season, player):
        template = jinja_environment.get_template('html/details.html')
        template_values = self.get_template_values(season, player)
        response.write(template.render(template_values))
