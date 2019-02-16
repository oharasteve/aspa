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
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users


import base_handler
import datetime
import webapp2

from data import players
from data import seasons
from data import clubs

TEMPLATE = 'html/edit_player.html'

class EditPlayer(base_handler.BaseHandler):
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
            'player': {
                'seasonName': self.request.get('season_select'),
                'player_select': self.request.get('player_select'),
                'firstName': self.request.get('firstName'),
                'lastName': self.request.get('lastName'),
                'phone': self.request.get('phone'),
                'email': self.request.get('email'),
            },
            'noseason': self.request.get('noseason'),
        }

        error_messages = []
        context_player = context['player']
        season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.startDate).get()
        player = players.Player.get_by_id(context_player['player_select'])
        if not player:
            error_messages.append("Missing player (%s)" % cgi.escape(
                context_player['player_select']))

        if len(error_messages) > 0:
            context['error_messages'] = error_messages
        else:
            player.firstName = context_player['firstName']
            player.lastName = context_player['lastName']
            player.phone = context_player['phone']
            player.email = context_player['email']
            player.put()

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
          'page_title': 'Edit Player',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'players': players.Player.getPlayers(),
          'club': club,
          'display_form': True,
          'player': {
                'season': '',
                'player_select': '',
                'firstName': '',
                'lastName': '',
                'handicap': '',
                'highRunTarget': '',
                'phone': '',
                'email': '',
                },
        }
        print context
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', EditPlayer)],
    debug=True,
    config=base_handler.CONFIG)
