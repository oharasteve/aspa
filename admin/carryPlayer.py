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
import webapp2

from data import players
from data import seasons
from data import stats
from data import clubs
import highRun

TEMPLATE = 'html/carry_player.html'

def most_recent_stat(x,y):
   if x.season.get().startDate < y.season.get().startDate:
      return y
   else:
      return x


class CarryPlayerHandler(base_handler.BaseHandler):
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
        context = {
            'seasons': seasons.Season.getSeasons(club),
            'club': club,
            'players': players.Player.getPlayers(),
            'seasonName': self.request.get('season_select'),
        }

        error_messages = []
        season = seasons.Season.get_by_id(context['seasonName'])
        additions = []

        for playerId in players.Player.getPlayers():
            checkbox = self.request.get('Carry_' + playerId['id'])
            if checkbox != '':
                player = players.Player.get_by_id(checkbox)
                dupStat = stats.PlayerSummary.query(
                    ndb.AND(stats.PlayerSummary.player == player.key, stats.PlayerSummary.season == season.key)).get()
                if dupStat:
                    error_messages.append("Duplicate player (%s) for season %s" % (cgi.escape(checkbox), season.name))
                else:
                    newStat = stats.PlayerSummary()
                    newStat.player = player.key
                    newStat.season = season.key
                    newStat.highRunTarget = highRun.getHighRunTarget(player.handicap)
                    newStat.wins = 0
                    newStat.forfeits = 0
                    newStat.losses = 0
                    newStat.highRun = 0
                    newStat.put()

                    additions.append("%s %s (%d, %.2f)" %
                        (player.firstName, player.lastName, player.handicap, newStat.highRunTarget))

        if len(error_messages) > 0:
            context['error_messages'] = error_messages
        else:
            context['additions'] = additions

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
        context = {
            'seasons': seasons.Season.getSeasons(club),
            'club': club,
            'players': players.Player.getPlayers(),
            'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', CarryPlayerHandler)],
    debug=True,
    config=base_handler.CONFIG)
