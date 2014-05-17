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
    def post(self):
        xseason = self.request.get('season_select')
        xclub = self.request.get('club_select')
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

        club = clubs.Club.get_by_id(xclub)
        if not club:
            error_messages.append("Club is required")

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
          'seasons': seasons.Season.getSeasons(),
          'players': players.Player.getPlayers(),
          'clubs': clubs.Club.getClubs(),
          'club': club,
          'season_selected': xseason,
          'club_selected': xclub,
          'display_form': True,
          'successfully_added_season_result': successfully_added_season_result,
          'error_messages': error_messages,
          'player': {
              'firstName': player.firstName,
              'lastName': player.lastName,
              }
        }

        self.render_response(TEMPLATE, **context)

    def get(self):
        season = seasons.Season.query().order(-seasons.Season.endDate).get();
        context = {
          'seasons': seasons.Season.getSeasons(),
          'season_selected': season.key,
          'players': players.Player.getPlayers(),
          'clubs': clubs.Club.getClubs(),
          'season_selected': season.key,
          'club_selected': 'LS',
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddSeasonResultHandler)],
    debug=True,
    config=base_handler.CONFIG)
