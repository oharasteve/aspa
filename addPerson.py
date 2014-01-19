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

class AddPersonHandler(webapp2.RequestHandler):
  def get(self):
    season = seasons.Season.get_by_id('Spr14')
      
app = webapp2.WSGIApplication([
  (r'/.*', AddPersonHandler)
], debug=True)


class AddPerson():
  def show(self, response):
    response.write('<hr/><form action="." method="post">\n')
    response.write('  <table>\n')
    response.write('    <tr><td rowspan=2>New Player\n')
    response.write('      <td>First: <input name="firstName" value="" size="20"/>\n')
    response.write('      <td class="right">Handicap: <input onchange=\'highRun("handicap","highRunTarget")\' id="handicap" name="handicap" value="" size="5"/>\n')
    response.write('      <td rowspan=2><input type="Button" value="Add New Player"/>\n')
    response.write('    <tr><td>Last: <input name="lastName" value="" size="20"/>\n')
    response.write('      <td class="right">High Run Target: <input id="highRunTarget" name="highRunTarget" value="" size="5"/>\n')
    response.write('  </table>\n')
    response.write('</form>\n')
