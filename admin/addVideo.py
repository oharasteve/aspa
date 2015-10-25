#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
from google.appengine.api import users

import base_handler
import datetime
import webapp2

from data import matches
from data import seasons
from data import clubs

TEMPLATE = 'html/add_video.html'

class AddVideoHandler(base_handler.BaseHandler):
    def post(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        user = users.get_current_user()
        if user not in club.owners and user.email().lower() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        xseason = self.request.get('season_select')
        xwhen = self.request.get('date')
        xseq = self.request.get('seq')
        xvideo1 = self.request.get('video1')
        xvideo2 = self.request.get('video2')

        error_messages = []
        try:
            when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid date: %s (%s)" % (cgi.escape(xwhen), err))

        season = seasons.Season.get_by_id(xseason)
        if not season:
            error_messages.append("Season is required")

        seq = int(xseq)
        display_form = False

        if not len(error_messages):
            # Update videos for the match
            matchList = matches.Match.query(
                ndb.AND(matches.Match.seq == seq,
                    matches.Match.date == when,
                    matches.Match.season == season.key)).fetch(1)
            if matchList:
              match = matchList[0]
              match.video1 = xvideo1
              match.video2 = xvideo2
              match.put()
              display_form = True
            else:
              error_messages.append("Unable to find #%d on %s" % (seq, when))

        context = {
          'page_title': 'Add a Video',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'seasons': seasons.Season.getSeasons(club),
          'club': club,
          'date': datetime.date.today().strftime('%Y-%m-%d'),
          'season_selected': season.key,
          'display_form': display_form,
          'error_messages': error_messages,
        }
        self.render_response(TEMPLATE, **context)

    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        user = users.get_current_user()
        if user not in club.owners and user.email().lower() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        season = seasons.Season.query().order(-seasons.Season.endDate).get();
        context = {
          'page_title': 'Add a Video',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'seasons': seasons.Season.getSeasons(club),
          'club': club,
          'date': datetime.date.today().strftime('%Y-%m-%d'),
          'season_selected': season.key,
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AddVideoHandler)],
    debug=True,
    config=base_handler.CONFIG)
