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
import datetime
import webapp2

from data import players

TEMPLATE = 'html/add_photo.html'

class AddPhotoHandler(base_handler.BaseHandler):
    def post(self):
        xplayer = self.request.get('player_select')
        xphoto = self.request.get('upload')

        error_messages = []
        player = players.Player.get_by_id(xplayer)
        if not player:
            error_messages.append("Player is required")

        display_form = False

        if not len(error_messages):
            # Update photo for the player
            playerList = players.Player.query(
                players.Player.key == player.key).fetch(1)
            if playerList:
              player = playerList[0]
              player.photo = xphoto
              player.put()
              display_form = True
            else:
              error_messages.append("Unable to find %s" % player)

        context = {
          'page_title': 'Add a Photo',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'players': players.Player.getPlayers(),
          'player_selected': player.key,
          'display_form': display_form,
          'error_messages': error_messages,
        }
        self.render_response(TEMPLATE, **context)

    def get(self):
        context = {
          'page_title': 'Add a Photo',
          'page_message': 'Click <a href="/admin">here</a> to go back to the admin page.',
          'players': players.Player.getPlayers(),
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddPhotoHandler)],
    debug=True,
    config=base_handler.CONFIG)
