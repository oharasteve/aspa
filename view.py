import datetime

import clubs
import highRun
import players
import seasons
import stats
import suggestMatch

class View():
  def header(self, response, season):
    response.write('<html>\n')
    response.write('<head>\n')
    
    response.write('<style type="text/css">\n')
    response.write('  table.details { border: 1px solid; }\n')
    response.write('  th.hdr { background-color: #e0e0e0; color: white; text-align: center; padding: 0 8px; }\n')
    response.write('  td { padding: 0 8px; }\n')
    response.write('  td.white { background-color: white; }\n')
    response.write('  td.gray{ background-color: #e0e0e0; }\n')
    response.write('  td.left { text-align: left; }\n')
    response.write('  td.center { text-align: center; }\n')
    response.write('  td.right { text-align: right; }\n')
    response.write('  input { text-align: center; }\n')
    response.write('</style>\n')
    
    response.write('<title>ASPA {0}</title>\n'.format(season.name))
    response.write('<script language="JavaScript1.2" src="/js/tablesort.js"></script>\n')
    response.write('<script language="javascript">\n')
    
    stats.insert(response)
    
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
    
    highRun.insert(response)
    
    suggestMatch.insert(response)

    response.write('</script>\n')
    response.write('</head>\n')
    response.write('<body bgcolor="#f0f0f0">\n')
    response.write('<center>\n')

    response.write('<h1>American Straight Pool Association</h1>\n')
    response.write('<h2>{0} : {1} to {2}</h2>\n'.format(season.name,
        season.startDate.strftime("%b %d, %Y"), season.endDate.strftime("%b %d, %Y")))
        
  def show(self, response, season):
    response.write('<table class="details">\n')
    response.write('  <thead><tr>\n')
    response.write('    <th class="hdr num">{0}</td>\n'.format('Seq'))
    response.write('    <th class="hdr nocase">{0}</td>\n'.format('First'))
    response.write('    <th class="hdr nocase">{0}</td>\n'.format('Last'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('H\'cap'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Won'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Lost'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Win %'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Points'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('High Run'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Target'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('% Goal'))
    response.write('  </tr></thead><tbody>\n')

    seq = 0
    for summary in stats.PlayerSummary.query(stats.PlayerSummary.season == season.key):
      player = players.Player.get_by_id(summary.player.id())
      points = 3 * summary.wins - summary.losses / 2.0 + (summary.wins + summary.losses) / 1000000.0
      goal = 100 * summary.highRun / summary.highRunTarget
      pct = 100 * summary.wins / (summary.wins + summary.losses)
      seq += 1
      
      response.write('  <tr>\n')
      response.write('    <td class="white center">{0}</td>\n'.format(seq))
      response.write('    <td class="white left">{0}</td>\n'.format(player.firstName))
      response.write('    <td class="white left">{0}</td>\n'.format(player.lastName))
      response.write('    <td class="white center">{0}</td>\n'.format(summary.handicap))
      response.write('    <td class="gray center">{0}</td>\n'.format(summary.wins))
      response.write('    <td class="gray center">{0}</td>\n'.format(summary.losses))
      response.write('    <td class="gray center">{:.2f}</td>\n'.format(pct))
      response.write('    <td class="gray right">{:.6f}</td>\n'.format(points))
      response.write('    <td class="white center">{0}</td>\n'.format(summary.highRun))
      response.write('    <td class="white center">{:.2f}</td>\n'.format(summary.highRunTarget))
      response.write('    <td class="white center">{:.2f}</td>\n'.format(goal))
      response.write('  </tr>\n')

    response.write('</tbody></table>\n')
    response.write('</center>\n')
    response.write('</br>\n')
    
  def footer(self, response):
    response.write('<hr/><font size=-1><i>League Manager: <a href="mailto:steve@oharasteve.com">CJ Robinson</a></i></font>\n')
    response.write('<br/><font size=-1><i>Web Issues: <a href="mailto:steve@oharasteve.com">steve@oharasteve.com</a></i></font>\n')
    response.write('</body>\n')
    response.write('</html>\n')
