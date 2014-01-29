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

import seasons

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        season = seasons.Season.get_by_id('Spr14')
        self.response.write('<html>\n')
        self.response.write('<head>\n')
        self.response.write('<title>ASPA {0}</title>\n'.format(season.name if season else ''))
        self.response.write('</head>\n')
        self.response.write('<body>\n')

        self.response.write('<p>Choices:<ul>\n')
        self.response.write('<li><a href="/">Home</a>\n')
        self.response.write('<li><a href="/admin/suggestMatch/">Suggest Match Targets</a>\n')
        self.response.write('<li><a href="/admin/addMatch/">Add Match Result</a>\n')
        self.response.write('<li><a href="/admin/addPlayer/">Add New Player</a>\n')
        self.response.write('<li><a href="/admin/addSeason/">Add New Season</a>\n')
        self.response.write('<li><a href="/admin/addClub/">Add New Club</a>\n')
        self.response.write('<li><a href="/admin/adjustHandicap/">Adjust Player Handicap</a>\n')
        self.response.write('<li><a href="/admin/destroy/">Delete All Data (careful!!!)</a>\n')
        self.response.write('<li><a href="/admin/regenerate/">Generate Three Weeks (once only)</a>\n')

        self.response.write('</body>\n')
        self.response.write('</html>\n')

app = webapp2.WSGIApplication([
  (r'/.*', AdminHandler)
], debug=True)
