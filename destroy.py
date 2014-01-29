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
import webapp2
from google.appengine.ext import ndb

import clubs
import highRun
import matches
import players
import seasons
import stats

class DestroyHandler(webapp2.RequestHandler):
    def get(self):
        # Delete all old data
        ndb.delete_multi(stats.PlayerSummary.query().fetch(keys_only=True))
        ndb.delete_multi(players.Player.query().fetch(keys_only=True))
        ndb.delete_multi(seasons.Season.query().fetch(keys_only=True))
        ndb.delete_multi(clubs.Club.query().fetch(keys_only=True))
        ndb.delete_multi(matches.Match.query().fetch(keys_only=True))
        ndb.delete_multi(highRun.HighRun.query().fetch(keys_only=True))

        self.response.write('<html>\n')
        self.response.write('<head>\n')
        self.response.write('</head>\n')
        self.response.write('<body>\n')
        self.response.write('<p>Data has been destroyed. Click <a href="/admin">here</a> to go back to the admin page.</p>\n')
        self.response.write('</body>\n')
        self.response.write('</html>\n')

app = webapp2.WSGIApplication([
   (r'/.*', DestroyHandler)
], debug=True)
