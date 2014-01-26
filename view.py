import cgi
import datetime

import players
import stats

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
    
    response.write('<title>ASPA {0}</title>\n'.format(season.name if season else ''))
    response.write('<script language="JavaScript1.2" src="/js/tablesort.js"></script>\n')
    response.write('</head>\n')
    response.write('<body bgcolor="#f0f0f0">\n')
    response.write('<center>\n')

    response.write('<h1>American Straight Pool Association</h1>\n')
    if season:
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

    if season:
      seq = 0
      for summary in stats.PlayerSummary.query(stats.PlayerSummary.season == season.key).order(-stats.PlayerSummary.wins).order(stats.PlayerSummary.losses):
        player = players.Player.get_by_id(summary.player.id())
        points = 3 * summary.wins - summary.losses / 2.0 + (summary.wins + summary.losses) / 1000000.0
        goal = 0.0
        if summary.highRunTarget > 0:
          goal = summary.highRun * 100.0 / summary.highRunTarget
        pct = 0.0
        if summary.wins > 0:
          pct = summary.wins * 100.0 / (summary.wins + summary.losses)
        seq += 1
        
        # For linking to detail page
        ref = 'details/?Season={0}&Player={1}'.format(cgi.escape(season.key.id()), cgi.escape(summary.player.id()))
        
        response.write('  <tr>\n')
        response.write('    <td class="white center"><a href="{1}">{0}</a></td>\n'.format(seq, ref))
        response.write('    <td class="white left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(player.firstName), ref))
        response.write('    <td class="white left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(player.lastName), ref))
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
    
