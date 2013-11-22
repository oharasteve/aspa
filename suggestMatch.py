import players

class SuggestMatch():
  def show(self, response, season):
    response.write('<hr/><table>\n')
    response.write('    <tr><td rowspan=2>Suggested Race:\n')
    
    response.write('    <td align="right">Player 1: \n')
    self.showNames(response, season, "playerA", "handicapA")
    response.write('      <td align="right">Handicap: <input id="handicapA" onchange="showMatches()" name="handicapA" value="" size="5"/>\n')
    for x in range(5, 15):
      response.write('      <td class="center" id="top_{0}0">\n'.format(x))
    
    response.write('    <tr><td align="right">Player 2: \n')
    self.showNames(response, season, "playerB", "handicapB")
    response.write('      <td align="right">Handicap: <input id="handicapB" onchange="showMatches()" name="handicapB" value="" size="5"/>\n')
    for x in range(5, 15):
      response.write('      <td class="center" id="bottom_{0}0">\n'.format(x))
    
    response.write('  </table>\n')

  def showNames(self, response, season, selectName, handicapName):
    response.write('      <select name="{0}" id="{1}" onchange=\'setHandicap("{2}", "{3}"); showMatches();\'>\n'.
        format(selectName, selectName, selectName, handicapName))
    response.write('        <option>Choose:</option>\n')
    for player in players.Player.query():
      response.write('        <option value="{0}">{1} {2}</option>\n'.format(player.key.id(), player.firstName, player.lastName))
    response.write('      </select>\n')

def insert(response):
  response.write('  function showMatches() {\n')
  response.write('    var handicapA = document.getElementById("handicapA").value;\n')
  response.write('    var handicapB = document.getElementById("handicapB").value;\n')
  response.write('    if (handicapA >= 100 && handicapA < 1000) {\n')
  response.write('      if (handicapB >= 100 && handicapB < 1000) {\n')
  response.write('        var delta = Math.abs(handicapA - handicapB);\n')
  response.write('        for (x=50; x<=140; x+=10) {\n')
  response.write('          var topElement = document.getElementById("top_"+x);\n')
  response.write('          var bottomElement = document.getElementById("bottom_"+x);\n')
  response.write('          var lower = Math.round(x / Math.pow(2, delta/100.0) / 5) * 5;\n')
  response.write('          if (lower > 5) {\n')
  response.write('            if (handicapA > handicapB) {\n')
  response.write('              topElement.innerHTML = x;\n')
  response.write('              bottomElement.innerHTML = lower;\n')
  response.write('            } else {\n')
  response.write('              topElement.innerHTML = lower;\n')
  response.write('              bottomElement.innerHTML = x;\n')
  response.write('            }\n')
  response.write('          } else {\n')
  response.write('            topElement.innerHTML = "";\n')
  response.write('            bottomElement.innerHTML = "";\n')
  response.write('          }\n')
  response.write('        }\n')
  response.write('        return;\n')
  response.write('      }\n')
  response.write('    }\n')
  response.write('    for (x=50; x<=140; x+=10) {\n')
  response.write('      var topElement = document.getElementById("top_"+x);\n')
  response.write('      var bottomElement = document.getElementById("bottom_"+x);\n')
  response.write('      topElement.innerHTML = "";\n')
  response.write('      bottomElement.innerHTML = "";\n')
  response.write('    }\n')
  response.write('  }\n')
