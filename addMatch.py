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
import time
import webapp2

import clubs
import players
import seasons
import stats

class AddMatchHandler(webapp2.RequestHandler):
  def get(self):
    season = seasons.Season.get_by_id('Spr14')

    self.response.write('<html>\n')
    self.response.write('<head>\n')
    self.response.write('<title>ASPA {0}</title>\n'.format(season.name))
    self.response.write('<style type="text/css">\n')
    self.response.write('  td { text-align: center; }\n')
    self.response.write('  input { text-align: center; }\n')
    self.response.write('</style>\n')
    self.response.write('<script language="javascript">\n')
    
    am = AddMatch()
    am.setHandicap(self.response)
    
    stats.insertJavascript(self.response)
    
    self.response.write('</script>\n')
    self.response.write('</head>\n')
    self.response.write('<body>\n')
    self.response.write('<h3>Add a match result</h3>\n')

    am.show(self.response, season)
    
    self.response.write('<p>Click <a href="/admin">here</a> to go back to the admin page.</p>\n')
    self.response.write('</body>\n')
    self.response.write('</html>\n')
      
app = webapp2.WSGIApplication([
  (r'/.*', AddMatchHandler)
], debug=True)


class AddMatch():
  def setHandicap(self, response):
    response.write('  function setHandicap(selectName, inputName) {\n')
    response.write('    var inputElement = document.getElementById(inputName);\n')
    response.write('    var selectElement = document.getElementById(selectName);\n')
    response.write('    if (!inputElement || !selectElement) {\n')
    response.write('      inputElement.value = "";\n')
    response.write('      return;\n')
    response.write('    }\n')
    response.write('    var playerCode = selectElement.options[selectElement.selectedIndex].value;\n')
    response.write('    inputElement.value = findHandicap(playerCode);\n')
    response.write('  }\n')

  def show(self, response, season):
    response.write('<form action="." method="post">\n')
    response.write('  <p>Date: <input name="date" value="{0}" size="10"/>\n'.format(time.strftime("%m/%d/%Y")))
    response.write('  <p>Club: \n')
    self.showClubs(response, 'club')
    response.write('  <p><table border>\n')
    response.write('    <tr><td align="right">Winner: \n')
    self.showNames(response, season, "nameW", "handicapW")
    response.write('      <td align="right">Loser: \n')
    self.showNames(response, season, "nameL", "handicapL")
    response.write('    <tr><td>Handicap: <input id="handicapW" name="handicapW" value="" size="5"/>\n')
    response.write('      <td>Handicap: <input id="handicapL" name="handicapL" value="" size="5"/>\n')
    response.write('    <tr><td>Target: <input name="targetW" value="" size="5"/>\n')
    response.write('      <td>Target: <input name="targetL" value="" size="5"/>\n')
    response.write('    <tr><td>Score: <input name="scoreW" value="" size="5"/>\n')
    response.write('      <td>Score: <input name="scoreL" value="" size="5"/>\n')
    response.write('    <tr><td>High Run: <input name="highRunW" value="" size="5"/>\n')
    response.write('      <td>High Run: <input name="highRunL" value="" size="5"/>\n')
    response.write('  </table>\n')
    response.write('  <p><input type="Button" value="Add Match Result"/>\n')
    response.write('</form>\n')

  def showClubs(self, response, selectName):
    response.write('      <select name="{0}" id="{0}">\n'.format(selectName))
    for club in clubs.Club.query():
      response.write('        <option value="{0}">{1}</option>\n'.format(club.key.id(), club.name))
    response.write('      </select>\n')

  def showNames(self, response, season, selectName, handicapName):
    response.write('      <select name="{0}" id="{0}" onchange=\'setHandicap("{0}", "{1}")\'>\n'.
        format(selectName, handicapName))
    response.write('        <option>Choose:</option>\n')
    for player in players.Player.query():
      response.write('        <option value="{0}">{1} {2}</option>\n'.format(player.key.id(), player.firstName, player.lastName))
    response.write('      </select>\n')
  