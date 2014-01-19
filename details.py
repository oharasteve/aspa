from google.appengine.ext import ndb
import webapp2

import matches
import players
import seasons

class DetailHandler(webapp2.RequestHandler):
  def get(self):
    season = seasons.Season.get_by_id(self.request.get('Season'))
    player = players.Player.get_by_id(self.request.get('Player'))
    
    # Show the webpage
    d = Details()
    d.header(self.response, season, player)
    d.show(self.response, season, player)
    d.footer(self.response)

app = webapp2.WSGIApplication([
   ('/details/', DetailHandler)
], debug=True)

class Details():
  def header(self, response, season, player):
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
    response.write('</head>\n')
    response.write('<body bgcolor="#f0f0f0">\n')
    response.write('<center>\n')

    response.write('<h1>ASPA {0} : {1} {2}</h1>\n'.format(season.name, player.firstName, player.lastName))
        
  def show(self, response, season, player):
    response.write('<table class="details">\n')
    response.write('  <thead><tr>\n')
    response.write('    <th class="hdr num">{0}</td>\n'.format('Date'))
    response.write('    <th class="hdr nocase">{0}</td>\n'.format('Result'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('H\'cap'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Points'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Target'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('High Run'))
    response.write('    <th class="hdr nocase">{0}</td>\n'.format('First'))
    response.write('    <th class="hdr nocase">{0}</td>\n'.format('Last'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('H\'cap'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Points'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('Target'))
    response.write('    <th class="hdr num">{0}</td>\n'.format('High Run'))
    response.write('  </tr></thead><tbody>\n')

    for match in matches.Match.query(ndb.OR(matches.Match.playerW == player.key, matches.Match.playerL == player.key)):
      response.write('  <tr>\n')
      response.write('    <td class="white center"><a href="/results/LSB_{0}.pdf">{0}</a></td>\n'.format(match.date, match.date))
      if (player.key == match.playerW):
        # For linking to opponent
        ref = '/details/?Season={0}&Player={1}'.format(season.key.id(), match.playerL.id())
        response.write('    <td class="white center">{0}</td>\n'.format('Won'))
        response.write('    <td class="white center">{0}</td>\n'.format(match.handicapW))
        response.write('    <td class="white center">{0}</td>\n'.format(match.scoreW))
        response.write('    <td class="white center">{0}</td>\n'.format(match.targetW))
        response.write('    <td class="white center">{0}</td>\n'.format(match.highRunW))
        loser = players.Player.get_by_id(match.playerL.id())
        response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(loser.firstName, ref))
        response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(loser.lastName, ref))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.handicapL))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.scoreL))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.targetL))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.highRunL))
      else:
        # For linking to opponent
        ref = '/details/?Season={0}&Player={1}'.format(season.key.id(), match.playerW.id())
        response.write('    <td class="white center">{0}</td>\n'.format('Lost'))
        response.write('    <td class="white center">{0}</td>\n'.format(match.handicapL))
        response.write('    <td class="white center">{0}</td>\n'.format(match.scoreL))
        response.write('    <td class="white center">{0}</td>\n'.format(match.targetL))
        response.write('    <td class="white center">{0}</td>\n'.format(match.highRunL))
        winner = players.Player.get_by_id(match.playerW.id())
        response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(winner.firstName, ref))
        response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(winner.lastName, ref))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.handicapW))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.scoreW))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.targetW))
        response.write('    <td class="gray center">{0}</td>\n'.format(match.highRunW))
      response.write('  </tr>\n')

    response.write('</tbody></table>\n')
    response.write('</center>\n')
    response.write('</br>\n')
    
  def footer(self, response):
    response.write('<hr/><font size=-1><i>League Manager: <a href="mailto:steve@oharasteve.com">CJ Robinson</a></i></font>\n')
    response.write('<br/><font size=-1><i>Web Issues: <a href="mailto:steve@oharasteve.com">steve@oharasteve.com</a></i></font>\n')
    response.write('</body>\n')
    response.write('</html>\n')
