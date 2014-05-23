"""Class to present the Player summary View."""

from google.appengine.ext import ndb

import base_handler
import cgi
import logging
import webapp2

from data import players
from data import seasons
from data import stats

TEMPLATE = 'html/view.html'


class ViewHandler(base_handler.BaseHandler):
    def get(self):
        seasonCode = self.request.GET.get('Season')
        season = None
        if seasonCode:
            season = seasons.Season.query(seasons.Season.key == ndb.Key(seasons.Season, seasonCode)).get();
        
        if not season:
            # Default to latest season
            season = seasons.Season.query().order(-seasons.Season.endDate).get();

        # Show the webpage
        context = View().get_context(season)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/', ViewHandler)],
    debug=True,
    config=base_handler.CONFIG)


class View():
    def get_context(self, season):
        player_summaries = []
        if season:
            seq = 0
            summaries = stats.PlayerSummary.query(stats.PlayerSummary.season
                    == season.key).order( -stats.PlayerSummary.wins).order(
                            stats.PlayerSummary.losses)
            for summary in summaries:
                player = players.Player.get_by_id(summary.player.id())
                seq += 1

                player_summary = {
                    'entry_index': seq,
                    'summary': summary,
                    'player': players.Player.get_by_id(summary.player.id()),
                    'details_page_url':
                    '/details/?Season={0}&Player={1}'.format(
                        cgi.escape(season.key.id()),
                        cgi.escape(summary.player.id())),
                    'season': season,
                    }
                player_summaries.append(player_summary)
        logging.debug('Found %d player summary records.' % (
            len(player_summaries)))

        context = {
                'seasonList': seasons.Season.getSeasons(),
                'season': season,
                'player_summaries': player_summaries,
                }
        return context
