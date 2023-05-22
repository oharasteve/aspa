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

from google.appengine.ext import blobstore

from data import clubs

TEMPLATE = 'html/weekly.html'

class WeeklyHandler(base_handler.BaseHandler):
    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        month = int(self.request.get('M'))
        day = int(self.request.get('D'))
        year = int(self.request.get('Y'))
        matchDate = datetime.date(year, month, day)

        # Show the webpage
        context = Weekly().get_context(matchDate, month, day, year, club)
        self.render_response(TEMPLATE, **context)

app = webapp2.WSGIApplication([(r'/([^/]*)/weekly/', WeeklyHandler)],
    debug=True,
    config=base_handler.CONFIG)

class Weekly():
    def get_context(self, matchDate, month, day, year, club):
        match_details = []
        weekly_matches = matches.Match.query(ndb.AND(
            matches.Match.club == club.key,
            matches.Match.date == matchDate)).order(matches.Match.seq)
        for match in weekly_matches:
            if match.scoreW is None:
                continue
            playerW = players.Player.get_by_id(match.playerW.id())
            playerL = players.Player.get_by_id(match.playerL.id())
            try:
                margin = match.targetL - match.scoreL
            except TypeError:
                margin = '??'

            match_summary = {
                'seq': match.seq,
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
                'margin': margin,
                'video1': match.video1,
                'video2': match.video2,
            }
            match_details.append(match_summary)

        # See if the pdf image is available
        blob_query = blobstore.BlobInfo.all()
        pdf_key = None
        # Use CJ's naming convention (two digit years, all data is 2010 or later)
        pdf_name = 'LSB Straight %d-%d-%d.pdf' % (month, day, (year % 100))
        pdf_blob = blob_query.filter('filename =', pdf_name).get()
        if pdf_blob:
          pdf_key = pdf_blob.key()

        context = {
                'matchDate': matchDate,
                'club': club,
                'match_details': match_details,
                'pdf_key': pdf_key,
                }
        return context
