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
import cgi
import datetime
import webapp2

import clubs
import matches
import players
import seasons
import stats

class AddMatchHandler(webapp2.RequestHandler):
  def post(self):
    club = clubs.Club.get_by_id('LS')
    season = seasons.Season.get_by_id('Spr14')
    self.header(self.response, season)
    
    xwhen = self.request.get('date')
    nameW = self.request.get('nameW')
    nameL = self.request.get('nameL')
    xhcapW = self.request.get('handicapW')
    xhcapL = self.request.get('handicapL')
    xtargetW = self.request.get('targetW')
    xtargetL = self.request.get('targetL')
    xscoreW = self.request.get('scoreW')
    xscoreL = self.request.get('scoreL')
    xhrunW = self.request.get('highRunW')
    xhrunL = self.request.get('highRunL')
    
    errmsg = ""
    try:
      when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
    except ValueError as err:
      errmsg += "<li>Invalid date: %s (%s)\n" % (cgi.escape(xwhen), err)

    winner = players.Player.get_by_id(nameW)
    if not winner:
      errmsg += "<li>Winner is required\n"
    loser = players.Player.get_by_id(nameL)
    if not loser:
      errmsg += "<li>Loser is required\n"

    if len(xhcapW) == 0:
      errmsg += "<li>Winner handicap is required\n"
    else:
      try:
        hcapW = int(xhcapW)
      except ValueError as err:
        errmsg += "<li>Invalid winner handicap: %s (%s)\n" % (cgi.escape(xhcapW), err)

    if len(xhcapL) == 0:
      errmsg += "<li>Loser handicap is required\n"
    else:
      try:
        hcapL = int(xhcapL)
      except ValueError as err:
        errmsg += "<li>Invalid loser handicap: %s (%s)\n" % (cgi.escape(xhcapL), err)

    if len(xtargetW) == 0:
      errmsg += "<li>Winner target is required\n"
    else:
      try:
        targetW = int(xtargetW)
      except ValueError as err:
        errmsg += "<li>Invalid winner target: %s (%s)\n" % (cgi.escape(xtargetW), err)

    if len(xtargetL) == 0:
      errmsg += "<li>Loser target is required\n"
    else:
      try:
        targetL = int(xtargetL)
      except ValueError as err:
        errmsg += "<li>Invalid loser target: %s (%s)\n" % (cgi.escape(xtargetL), err)

    if len(xscoreW) == 0:
      errmsg += "<li>Winner score is required\n"
    else:
      try:
        scoreW = int(xscoreW)
      except ValueError as err:
        errmsg += "<li>Invalid winner score: %s (%s)\n" % (cgi.escape(xscoreW), err)

    if len(xscoreL) == 0:
      errmsg += "<li>Loser score is required\n"
    else:
      try:
        scoreL = int(xscoreL)
      except ValueError as err:
        errmsg += "<li>Invalid loser score: %s (%s)\n" % (cgi.escape(xscoreL), err)

    if len(xhrunW) == 0:
      hrunW = 0
    else:
      try:
        hrunW = int(xhrunW)
      except ValueError as err:
        errmsg += "<li>Invalid winner high run: %s (%s)\n" % (cgi.escape(xhrunW), err)

    if len(xhrunL) == 0:
      hrunL = 0
    else:
      try:
        hrunL = int(xhrunL)
      except ValueError as err:
        errmsg += "<li>Invalid loser high run: %s (%s)\n" % (cgi.escape(xhrunL), err)

    if not errmsg:
      if scoreW != targetW:
        errmsg += "<li>Winner score (%s) does not match target (%s)\n" % (scoreW, targetW)
      if scoreL >= targetL:
        errmsg += "<li>Loser score (%s) is too high (%s)\n" % (scoreL, targetL)
        
    if errmsg:
      self.response.write("<h3><font color=red>Errors:<ul>%s</ul></font></h3>\n" % errmsg)
      self.shared(self.response, xwhen, nameW, nameL, xhcapW, xhcapL, xtargetW, xtargetL, xscoreW, xscoreL, xhrunW, xhrunL)
    else:
      match = matches.Match()
      match.date = when
      match.season = season.key
      match.club = club.key
      
      match.playerW = winner.key
      match.handicapW = hcapW
      match.scoreW = scoreW
      match.targetW = targetW
      match.highRunW = hrunW
      
      match.playerL = loser.key
      match.handicapL = hcapL
      match.scoreL = scoreL
      match.targetL = targetL
      match.highRunL = hrunL
      
      match.put()

      # Update statistics for the winner and loser
      winnerStats = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerW).fetch(1)[0]
      loserStats = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerL).fetch(1)[0]
      
      # Update win / loss totals
      winnerStats.wins = winnerStats.wins + 1
      loserStats.losses = loserStats.losses + 1

      # Update handicaps
      winnerStats.handicap = winnerStats.handicap + 3
      loserStats.handicap = loserStats.handicap - 3

      # Update high runs
      if hrunW > winnerStats.highRun:
        winnerStats.highRun = hrunW
      if hrunL > loserStats.highRun:
        loserStats.highRun = hrunL
      
      winnerStats.put()
      loserStats.put()

      self.response.write('<h3>Successfully added new Match: %s beat %s</h3><hr/>\n' % (cgi.escape(winner.firstName), cgi.escape(loser.firstName)))
      self.shared(self.response, when.strftime("%Y-%m-%d"), "", "", "", "", "", "", "", "", "", "")
    self.footer(self.response)
  
  def get(self):
    season = seasons.Season.get_by_id('Spr14')
    self.header(self.response, season)
    today = datetime.date.today()
    self.shared(self.response, today.strftime("%Y-%m-%d"), "", "", "", "", "", "", "", "", "", "")
    self.footer(self.response)
    
  def header(self, response, season):
    self.response.write('<html>\n')
    self.response.write('<head>\n')
    self.response.write('<title>ASPA {0}</title>\n'.format(cgi.escape(season.name)))
    self.response.write('<style type="text/css">\n')
    self.response.write('  td { text-align: center; }\n')
    self.response.write('  input { text-align: center; }\n')
    self.response.write('</style>\n')
    self.response.write('<script language="javascript">\n')
    
    self.setHandicap(self.response)
    
    stats.insertJavascript(self.response)
    
    self.response.write('</script>\n')
    self.response.write('</head>\n')
    self.response.write('<body>\n')

  def footer(self, response):
    response.write('</body>\n')
    response.write('</html>\n')

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
    
  def shared(self, response, when, winner, loser, hcapW, hcapL, targetW, targetL, scoreW, scoreL, hrunW, hrunL):
    response.write('<h3>Add a match result</h3>\n')
    response.write('<form action="." method="post">\n')
    response.write('  <p>Date: <input name="date" value="{0}" size="10"/>\n'.format(when))
    response.write('  <p>Club: \n')
    self.showClubs(response, 'club')
    response.write('  <p><table border>\n')
    response.write('    <tr><td align="right">Winner: \n')
    self.showNames(response, "nameW", "handicapW", winner)
    response.write('      <td align="right">Loser: \n')
    self.showNames(response, "nameL", "handicapL", loser)
    response.write('    <tr><td>Handicap: <input id="handicapW" name="handicapW" value="%s" size="5"/>\n' % cgi.escape(hcapW))
    response.write('      <td>Handicap: <input id="handicapL" name="handicapL" value="%s" size="5"/>\n' % cgi.escape(hcapL))
    onChangeTargetW = "onchange=\"scoreW.value = this.value;\""
    response.write('    <tr><td>Target: <input name="targetW" value="%s" size="5" %s/>\n' % (cgi.escape(targetW), onChangeTargetW))
    response.write('      <td>Target: <input name="targetL" value="%s" size="5"/>\n' % cgi.escape(targetL))
    response.write('    <tr><td>Score: <input name="scoreW" value="%s" size="5"/>\n' % cgi.escape(scoreW))
    response.write('      <td>Score: <input name="scoreL" value="%s" size="5"/>\n' % cgi.escape(scoreL))
    response.write('    <tr><td>High Run: <input name="highRunW" value="%s" size="5"/>\n' % cgi.escape(hrunW))
    response.write('      <td>High Run: <input name="highRunL" value="%s" size="5"/>\n' % cgi.escape(hrunL))
    response.write('  </table>\n')
    response.write('<p>\n')
    response.write('  <input type="button" value="Done" onclick="window.location=\'/admin\'">\n')
    response.write('  <input type="submit" value="Submit">\n')
    response.write('</form>\n')

  def showClubs(self, response, selectName):
    response.write('      <select name="{0}" id="{0}">\n'.format(selectName))
    for club in clubs.Club.query():
      response.write('        <option value="{0}">{1}</option>\n'.format(cgi.escape(club.key.id()), cgi.escape(club.name)))
    response.write('      </select>\n')

  def showNames(self, response, selectName, handicapName, selection):
    response.write('      <select name="{0}" id="{0}" onchange=\'setHandicap("{0}", "{1}")\'>\n'.
        format(selectName, handicapName))
    response.write('        <option>Choose:</option>\n')
    for player in players.Player.query():
      id = player.key.id()
      sel = " selected" if selection == id else ""
      response.write('        <option value="{0}"{3}>{1} {2}</option>\n'.format(
          cgi.escape(id), cgi.escape(player.firstName), cgi.escape(player.lastName), sel))
    response.write('      </select>\n')
        
app = webapp2.WSGIApplication([
  (r'/.*', AddMatchHandler)
], debug=True)
