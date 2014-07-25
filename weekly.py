"""Class to present the Weekly summary View."""

from google.appengine.ext import ndb

import base_handler
import cgi
import datetime
import logging
import webapp2

from data import matches
from data import players
from data import seasons

TEMPLATE = 'html/weekly.html'


class WeeklyHandler(base_handler.BaseHandler):
    def get(self):
        month = int(self.request.get('M'))
        day = int(self.request.get('D'))
        year = int(self.request.get('Y'))
        matchDate = datetime.date(year, month, day)

        # Show the webpage
        context = Weekly().get_context(matchDate)
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/weekly/', WeeklyHandler)],
    debug=True,
    config=base_handler.CONFIG)


class Weekly():
    def get_context(self, matchDate):
        match_details = []
        seq = 0
        weekly_matches = matches.Match.query(
            matches.Match.date == matchDate).order(matches.Match.seq)
        for match in weekly_matches:
            seq += 1
            playerW = players.Player.get_by_id(match.playerW.id())
            playerL = players.Player.get_by_id(match.playerL.id())

            match_summary = {
                'seq': seq,
                'playerW': playerW,
                'handicapW': match.handicapW,
                'scoreW': match.scoreW,
                'targetW': match.targetW,
                'highRunW': match.highRunW,
                'forfeited': match.forfeited,
                'playerL': playerL,
                'handicapL': match.handicapL,
                'scoreL': match.scoreL,
                'targetL': match.targetL,
                'highRunL': match.highRunL,
            }
            match_details.append(match_summary)
        pdf_url = '/results/LSB_{0}.pdf'.format(matchDate)

        context = {
                'matchDate': matchDate,
                'match_details': match_details,
                'pdf_url': pdf_url,
                }
        return context
