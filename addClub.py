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

class AddClubHandler(webapp2.RequestHandler):
  def get(self):
    season = seasons.Season.get_by_id('Spr14')

    self.response.write('<html>\n')
    self.response.write('<head>\n')
    self.response.write('<title>ASPA {0}</title>\n'.format(season.name))
    self.response.write('</head>\n')
    self.response.write('<body>\n')
    self.response.write('<h3>Add a new Club</h3>\n')

    self.response.write('<h3><i>Not yet implemented.</i></h3>\n')
    
    self.response.write('<p>Click <a href="/admin">here</a> to go back to the admin page.</p>\n')
    self.response.write('</body>\n')
    self.response.write('</html>\n')
      
app = webapp2.WSGIApplication([
  (r'/.*', AddClubHandler)
], debug=True)
