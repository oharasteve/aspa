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

import adjustments
import players
import stats

class AdjustHandicapHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write('<html>\n')
        self.response.write('<head>\n')
        self.response.write('<title>ASPA</title>\n')
        self.response.write('</head>\n')
        self.response.write('<body>\n')
        self.response.write('<h3>Adjust a Handicap</h3>\n')

        self.response.write('<h3><i>Not yet implemented.</i></h3>\n')
        self.response.write('<p>Click <a href="/admin">here</a> to go back to the admin page.</p>\n')

        self.response.write('</body>\n')
        self.response.write('</html>\n')

app = webapp2.WSGIApplication([
  (r'/.*', AdjustHandicapHandler)
], debug=True)
