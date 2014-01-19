import time

import clubs
import players

class AddMatch():
  def show(self, response, season):
    response.write('<hr/><form action="." method="post">\n')
    response.write('  <table>\n')
    response.write('    <tr><td>Date: <input name="date" value="{0}" size="10"/>\n'.format(time.strftime("%m/%d/%Y")))
    response.write('      <td align="right">Winner: \n')
    self.showNames(response, season, "nameW", "handicapW")
    response.write('      <td>Handicap: <input id="handicapW" name="handicapW" value="" size="5"/>\n')
    response.write('      <td>Target: <input name="targetW" value="" size="5"/>\n')
    response.write('      <td>Score: <input name="scoreW" value="" size="5"/>\n')
    response.write('      <td>High Run: <input name="highRunW" value="" size="5"/>\n')
    response.write('      <td rowspan=2><input type="Button" value="Add Match Result"/>\n')
    response.write('    <tr><td>Club: \n')
    self.showClubs(response, 'club')
    response.write('      <td align="right">Loser: \n')
    self.showNames(response, season, "nameL", "handicapL")
    response.write('      <td>Handicap: <input id="handicapL" name="handicapL" value="" size="5"/>\n')
    response.write('      <td>Target: <input name="targetL" value="" size="5"/>\n')
    response.write('      <td>Score: <input name="scoreL" value="" size="5"/>\n')
    response.write('      <td>High Run: <input name="highRunL" value="" size="5"/>\n')
    response.write('  </table>\n')
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
  