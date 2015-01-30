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
import cgi
import datetime
import logging
import webapp2

from data import clubs
from data import matches
from data import players
from data import seasons
from data import stats

TEMPLATE = 'html/add_season_result.html'

class AddSeasonResultHandler(base_handler.BaseHandler):
    def post(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        user = users.get_current_user()
        if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        xseason = self.request.get('season_select')
        xname = self.request.get('player_select')
        xhcap = self.request.get('player_handicap')
        xwins = self.request.get('player_wins')
        xlosses = self.request.get('player_losses')
        xforfeits = self.request.get('player_forfeits')
        xhighrun = self.request.get('player_highrun')
        xhighruntarget = self.request.get('player_highrun_target')

        successfully_added_season_result = False
        error_messages = []

        player = players.Player.get_by_id(xname)
        if not player:
            error_messages.append("Player is required")

        season = seasons.Season.get_by_id(xseason)
        if not season:
            error_messages.append("Season is required")

        if not len(error_messages):
            # Create statistics for the player
            summary = stats.PlayerSummary()
            
            summary.player = player.key
            summary.season = season.key
            summary.handicap = int(xhcap)
            summary.wins = int(xwins)
            summary.losses = int(xlosses)
            summary.forfeits = int(xforfeits)
            summary.highRun = int(xhighrun)
            summary.highRunTarget = float(xhighruntarget)

            summary.put()
            successfully_added_season_result = True

        context = {
          'seasons': seasons.Season.getSeasons(club),
          'players': stats.PlayerSummary.getPlayers(season),
          'clubs': clubs.Club.getClubs(),
          'club': club,
          'season_selected': xseason,
          'club_selected': club,
          'display_form': True,
          'successfully_added_season_result': successfully_added_season_result,
          'error_messages': error_messages,
          'player': {
              'firstName': player.firstName,
              'lastName': player.lastName,
              }
        }

        self.render_response(TEMPLATE, **context)

    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        user = users.get_current_user()
        if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.startDate).get();
        context = {
          'seasons': seasons.Season.getSeasons(club),
          'club': club,
          'season_selected': season.key,
          'players': stats.PlayerSummary.getPlayers(season),
          'clubs': clubs.Club.getClubs(),
          'season_selected': season.key,
          'club_selected': 'LS',
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AddSeasonResultHandler)],
    debug=True,
    config=base_handler.CONFIG)
