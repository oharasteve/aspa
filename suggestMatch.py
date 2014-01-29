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

import players
import seasons
import stats

class SuggestMatchHandler(webapp2.RequestHandler):
    def get(self):
        season = seasons.Season.get_by_id('Spr14')
        sm = SuggestMatch()

        self.response.write('<html>\n')
        self.response.write('<head>\n')
        self.response.write('<title>ASPA {0}</title>\n'.format(season.name))
        self.response.write('<style type="text/css">\n')
        self.response.write('  td { text-align: center; }\n')
        self.response.write('  input { text-align: center; }\n')
        self.response.write('</style>\n')
        self.response.write('<script language="javascript">\n')

        sm.setHandicap(self.response)
        sm.showMatches(self.response)

        stats.insertJavascript(self.response)

        self.response.write('</script>\n')
        self.response.write('</head>\n')
        self.response.write('<body>\n')

        sm.show(self.response, season)

        self.response.write('<p><input type="button" value="Done" onclick="window.location=\'/admin\'">\n')
        self.response.write('</body>\n')
        self.response.write('</html>\n')

class SuggestMatch():
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
        response.write('    showMatches();\n')
        response.write('  }\n')

    def show(self, response, season):
        response.write('<h3>Suggested Race:</h3>\n')
        response.write('<table border>\n')
        response.write('  <tr><td>Player 1: \n')
        self.showNames(response, season, "playerA", "handicapA")
        response.write('    <td>Player 2: \n')
        self.showNames(response, season, "playerB", "handicapB")
        response.write('  <tr><td>Handicap: <input id="handicapA" onchange="showMatches()" name="handicapA" value="" size="5"/>\n')
        response.write('    <td>Handicap: <input id="handicapB" onchange="showMatches()" name="handicapB" value="" size="5"/>\n')
        for x in range(5, 15):
            response.write('  <tr><td id="A_{0}0">&nbsp;\n'.format(x))
            response.write('    <td id="B_{0}0">&nbsp;\n'.format(x))
        response.write('</table>\n')

    def showNames(self, response, season, selectName, handicapName):
        response.write('    <select name="{0}" id="{1}" onchange=\'setHandicap("{2}", "{3}");\'>\n'.
            format(selectName, selectName, selectName, handicapName))
        response.write('      <option>Choose:</option>\n')
        for player in players.Player.query():
            response.write('      <option value="{0}">{1} {2}</option>\n'.format(player.key.id(), player.firstName, player.lastName))
        response.write('    </select>\n')

    def showMatches(self, response):
        response.write('  function showMatches() {\n')
        response.write('    var handicapA = document.getElementById("handicapA").value;\n')
        response.write('    var handicapB = document.getElementById("handicapB").value;\n')
        response.write('    if (handicapA >= 100 && handicapA < 1000) {\n')
        response.write('      if (handicapB >= 100 && handicapB < 1000) {\n')
        response.write('        var delta = Math.abs(handicapA - handicapB);\n')
        response.write('        for (x=50; x<=140; x+=10) {\n')
        response.write('          var elementA = document.getElementById("A_"+x);\n')
        response.write('          var elementB = document.getElementById("B_"+x);\n')
        response.write('          var lower = Math.round(x / Math.pow(2, delta/100.0) / 5) * 5;\n')
        response.write('          if (lower > 5) {\n')
        response.write('            if (handicapA > handicapB) {\n')
        response.write('              elementA.innerHTML = x;\n')
        response.write('              elementB.innerHTML = lower;\n')
        response.write('            } else {\n')
        response.write('              elementA.innerHTML = lower;\n')
        response.write('              elementB.innerHTML = x;\n')
        response.write('            }\n')
        response.write('          } else {\n')
        response.write('            elementA.innerHTML = "&nbsp;";\n')
        response.write('            elementB.innerHTML = "&nbsp;";\n')
        response.write('          }\n')
        response.write('        }\n')
        response.write('        return;\n')
        response.write('      }\n')
        response.write('    }\n')
        response.write('    for (x=50; x<=140; x+=10) {\n')
        response.write('      var ElementA = document.getElementById("A_"+x);\n')
        response.write('      var ElementB = document.getElementById("B_"+x);\n')
        response.write('      ElementA.innerHTML = "&nbsp;";\n')
        response.write('      ElementB.innerHTML = "&nbsp;";\n')
        response.write('    }\n')
        response.write('  }\n')

app = webapp2.WSGIApplication([
  (r'/.*', SuggestMatchHandler)
], debug=True)
