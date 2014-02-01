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
import base_handler
import clubs
import players
import seasons
import stats
import webapp2

TEMPLATE = 'html/suggest_match.html'

class SuggestMatchHandler(base_handler.BaseHandler):
    def get(self):
        season = seasons.Season.get_by_id('Spr14')
        context = {
          'season': seasons.Season.get_by_id('Spr14'),
          'players': players.Player.getPlayers(),
          'player_summaries': stats.PlayerSummary.getPlayerSummaries(),
          'clubs': clubs.Club.getClubs(),
          'playerA_selectedIndex': -1,
          'playerB_selectedIndex': -1,
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', SuggestMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
