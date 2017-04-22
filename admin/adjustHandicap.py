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

from data import adjustments
from data import players
from data import seasons
from data import stats
from data import clubs

TEMPLATE = 'html/adjust_handicap.html'

class AdjustHandicapHandler(base_handler.BaseHandler):
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
        xwhen = self.request.get('todays_date')
        xname = self.request.get('player_select')
        xhcapNew = self.request.get('newHandicap')
        xhrtOld = self.request.get('oldHighRunTarget')
        xhrtNew = self.request.get('newHighRunTarget')
        comment = self.request.get('comment')

        error_messages = []
        try:
            when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid date: %s (%s)" % (cgi.escape(xwhen), err))

        player = players.Player.get_by_id(xname)
        if not player:
            error_messages.append("Player is required")

        season = seasons.Season.get_by_id(xseason)
        if not season:
            error_messages.append("Season is required")

        hcapNew = int(xhcapNew)
        hrtOld = float(xhrtOld)
        hrtNew = float(xhrtNew)

        if not len(error_messages):
            adjustment = adjustments.Adjustment()
            adjustment.date = when
            adjustment.season = season.key
            adjustment.player = player.key
            adjustment.oldHandicap = 0
            adjustment.newHandicap = hcapNew
            adjustment.oldHighRunTarget = hrtOld
            adjustment.newHighRunTarget = hrtNew
            adjustment.comment = comment
            adjustment.put()

            # Update statistics for the player
            playerStats = stats.PlayerSummary.query(
                ndb.AND(stats.PlayerSummary.player == player.key, stats.PlayerSummary.season == season.key)).fetch(1)[0]
            player.handicap = hcapNew
            playerStats.highRunTarget = hrtNew
            playerStats.put()
            player.put()
        
        context = {
          'page_title': 'Adjust a Handicap',
          'seasons': seasons.Season.getSeasons(club),
          'club': club,
          'todays_date': datetime.date.today().strftime('%Y-%m-%d'),
          'players': players.Player.getPlayers(),
          'player_summaries': stats.PlayerSummary.getPlayerSummaries(season),
          'season_selected': season.key,
          'player_selectedIndex': -1,
          'display_form': True,
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
          'page_title': 'Adjust a Handicap',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'seasons': seasons.Season.getSeasons(club),
          'club': club,
          'todays_date': datetime.date.today().strftime('%Y-%m-%d'),
          'players': players.Player.getPlayers(),
          'player_summaries': stats.PlayerSummary.getPlayerSummaries(season),
          'season_selected': season.key,
          'player_selectedIndex': -1,
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AdjustHandicapHandler)],
    debug=True,
    config=base_handler.CONFIG)
