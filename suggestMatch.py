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
import webapp2

from data import clubs
from data import players
from data import seasons
from data import stats


TEMPLATE = 'html/suggest_match.html'

class SuggestMatchHandler(base_handler.BaseHandler):
    def get(self):
        players_data = []
        for player in players.Player.query():
            # TODO: Get stats from user provided season.
            player_summary = stats.PlayerSummary.query(stats.PlayerSummary.player == player.key).fetch(1)[0]
            players_data.append({
                'playerId': player.key.id(),
                'firstName': str(player.firstName),
                'lastName': str(player.lastName),
                'fullName': str('%s %s' % (player.firstName, player.lastName)),
                'handicap': player_summary.handicap,
                })

        context = {
          'seasons': seasons.Season.getSeasons(),
          'players': players_data,
          'clubs': clubs.Club.getClubs(),
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', SuggestMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
