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
import webapp2

from data import players
from data import seasons
from data import stats

TEMPLATE = 'html/add_player.html'

class AddPersonHandler(base_handler.BaseHandler):
    def post(self):
        context = {
            'seasons': seasons.Season.getSeasons(),
            'player': {
                'seasonName': self.request.get('season_select'),
                'code': self.request.get('code'),
                'firstName': self.request.get('firstName'),
                'lastName': self.request.get('lastName'),
                'handicap': self.request.get('handicap'),
                'highRunTarget': self.request.get('highRunTarget'),
                'phone': self.request.get('phone'),
                'email': self.request.get('email'),
            },
            'noseason': self.request.get('noseason'),
        }

        error_messages = []
        context_player = context['player']
        season = seasons.Season.get_by_id(context_player['seasonName'])
        player = players.Player.get_by_id(context_player['code'])
        if player:
            error_messages.append("Duplicate player (%s)" % cgi.escape(
                context_player['code']))
        handicap = int(context_player['handicap'])
        highRunTarget = float(context_player['highRunTarget'])
        noseason = (self.request.get('noseason') == 'on')

        if len(error_messages) > 0:
            context['error_messages'] = error_messages
        else:
            player = players.Player(key=ndb.Key(players.Player,
                context_player['code']))
            player.firstName = context_player['firstName']
            player.lastName = context_player['lastName']
            player.phone = context_player['phone']
            player.email = context_player['email']
            player.put()

            if not noseason:
                stat = stats.PlayerSummary()
                stat.player = player.key
                stat.season = season.key
                stat.handicap = int(context_player['handicap'])
                stat.highRunTarget = float(context_player['highRunTarget'])
                stat.highRun = 0
                stat.wins = 0
                stat.losses = 0
                stat.put()

        self.render_response(TEMPLATE, **context)

    def get(self):
        context = {
            'seasons': seasons.Season.getSeasons(),
            'player': {
                'season': '',
                'code': '',
                'firstName': '',
                'lastName': '',
                'handicap': '',
                'highRunTarget': '',
                'phone': '',
                'email': '',
                },
            'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddPersonHandler)],
    debug=True,
    config=base_handler.CONFIG)
