from google.appengine.ext import ndb

import base_handler
import cgi
import webapp2
import base64

from data import matches
from data import players
from data import seasons
from data import stats
from data import clubs

TEMPLATE = 'html/details.html'

class DetailsHandler(base_handler.BaseHandler):
    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        season = seasons.Season.get_by_id(self.request.get('Season'))
        player = players.Player.get_by_id(self.request.get('Player'))

        # Show the webpage
        context = Details().get_context(season, player)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/details/', DetailsHandler)],
    debug=True,
    config=base_handler.CONFIG)

class Details():
    def get_match_details(self, season, player):
        entries = []
        seq = 0
        season_matches = matches.Match.query( ndb.AND( ndb.OR(
            matches.Match.playerW == player.key, matches.Match.playerL ==
            player.key), stats.PlayerSummary.season == season.key
            )).order(matches.Match.date, matches.Match.seq)
        for match in season_matches:
            if match.scoreW is None:
                continue
            seq += 1
            match_data = matches.match_util(match)
            if player.key == match_data['winner']['player']:
                participant = match_data['winner']
                opponent = match_data['loser']
                result = 'Won'
                try:
                    win_mgn = opponent['target'] - opponent['score']
                except TypeError:
                    win_mgn = repr(opponent['target']) + ' - ' + repr(opponent['score'])
                lose_mgn = ''
            else:
                participant = match_data['loser']
                opponent = match_data['winner']
                try:
                    lose_mgn = participant['target'] - participant['score']
                except TypeError:
                    lose_mgn = repr(participant['target']) + ' - ' + repr(participant['score'])
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
                    'seq': match.seq,
                    'results_pdf_url': '/%s/weekly/?Y=%d&M=%d&D=%d' %
                        (cgi.escape(match_data['club'].id()),
                        match.date.year, match.date.month, match.date.day),
                    'date': match.date,
                    'result': result,
                    'player': participant,
                    'opponent': opponent,
                    'win_mgn': win_mgn,
                    'lose_mgn': lose_mgn,
                    'opponent_details_page_url':
                    '/{2}/details/?Season={0}&Player={1}'.format(
                        cgi.escape(season.key.id()),
                        cgi.escape(opponent['player'].id()),
                        cgi.escape(match_data['club'].id())),
                    'video1': match.video1,
                    'video2': match.video2,
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
        if summary.handicap == None:
            summary.handicap = player.handicap;
            summary.put()
        lifetime = seasons.Season.get_by_id('lifetime')
        lifesummary = {}
        if lifetime:
           lifesummary = self.get_summary(lifetime, player)
        context = {
                'season': season,
                'match_details': match_details,
                'player': player,
                'club': season.club,
                'summary': summary,
                'lifesummary': lifesummary,
                'charts_page_url':
                '/{1}/charts/?Player={0}'.format(
                    player.key.id(),
                    season.club.id(),
                    ),
                }
        return context
