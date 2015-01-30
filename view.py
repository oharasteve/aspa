"""Class to present the Player summary View."""

from google.appengine.ext import ndb

import base_handler
import cgi
import logging
import webapp2

from data import players
from data import matches
from data import seasons
from data import stats
from data import clubs

TEMPLATE = 'html/view.html'

class ViewHandler(base_handler.BaseHandler):
    def get(self):
      pass

class ViewClubHandler(base_handler.BaseHandler):
    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        seasonCode = self.request.GET.get('Season')
        season = None
        if seasonCode:
            season = seasons.Season.query(seasons.Season.key == ndb.Key(seasons.Season, seasonCode)).get();
        
        if not season:
            # Default to latest season
            season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.startDate).get()

        # Show the webpage
        context = View().get_context(season, club)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([
            (r'/([^/]*)/', ViewClubHandler),
            (r'/', ViewHandler)
            ],
    debug=True,
    config=base_handler.CONFIG)


class View():
    def get_context(self, season, club):
        player_summaries = []
        if season:
            seq = 0
            matchCount = 0
            if season.key.id() == 'lifetime':
                summaries = stats.PlayerSummary.query(stats.PlayerSummary.season
                    == season.key).order( -stats.PlayerSummary.pct)
            else:
                summaries = stats.PlayerSummary.query(stats.PlayerSummary.season
                    == season.key).order( -stats.PlayerSummary.points)
            for summary in summaries:
                player = players.Player.get_by_id(summary.player.id())
                seq += 1
                matchCount += summary.wins

                player_summary = {
                    'entry_index': seq,
                    'summary': summary,
                    'player': players.Player.get_by_id(summary.player.id()),
                    'details_page_url':
                    '/{2}/details/?Season={0}&Player={1}'.format(
                        cgi.escape(season.key.id()),
                        cgi.escape(summary.player.id()),
                        cgi.escape(club.key.id()),
                        ),
                    'season': season,
                    'club': club,
                    }
                player_summaries.append(player_summary)

            weekCount = matches.Match.query(
                matches.Match.season == season.key, projection=["date"], distinct=True).count()
            
        logging.debug('Found %d player summary records.' % (
            len(player_summaries)))

        context = {
                'seasonList': seasons.Season.getSeasons(club),
                'season': season,
                'club': club,
                'player_summaries': player_summaries,
                'weeks': weekCount,
                'matches': matchCount,
                }
        return context
