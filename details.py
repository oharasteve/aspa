from google.appengine.ext import ndb
import cgi
import webapp2

import matches
import players
import seasons
import shared
import stats

class DetailHandler(webapp2.RequestHandler):
    def get(self):
        season = seasons.Season.get_by_id(self.request.get('Season'))
        player = players.Player.get_by_id(self.request.get('Player'))

        # Show the webpage
        d = Details()
        d.header(self.response, season, player)
        d.show(self.response, season, player)
        shared.footer(self.response)

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

        response.write('<title>ASPA {0}</title>\n'.format(cgi.escape(season.name)))
        response.write('<script language="JavaScript1.2" src="/js/tablesort.js"></script>\n')
        response.write('</head>\n')
        response.write('<body bgcolor="#f0f0f0">\n')
        response.write('<center>\n')

        response.write('<h1>ASPA {0} : {1} {2}</h1>\n'.format(cgi.escape(season.name), cgi.escape(player.firstName), cgi.escape(player.lastName)))

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

        for match in matches.Match.query(ndb.AND(ndb.OR(matches.Match.playerW == player.key, matches.Match.playerL == player.key), stats.PlayerSummary.season == season.key)).order(matches.Match.date):
            response.write('  <tr>\n')
            response.write('    <td class="white center"><a href="/results/LSB_{0}.pdf">{0}</a></td>\n'.format(match.date, match.date))
            if (player.key == match.playerW):
                # For linking to opponent
                ref = '/details/?Season={0}&Player={1}'.format(cgi.escape(season.key.id()), cgi.escape(match.playerL.id()))
                response.write('    <td class="white center">{0}</td>\n'.format('Won'))
                response.write('    <td class="white center">{0}</td>\n'.format(match.handicapW))
                response.write('    <td class="white center">{0}</td>\n'.format(match.scoreW))
                response.write('    <td class="white center">{0}</td>\n'.format(match.targetW))
                response.write('    <td class="white center">{0}</td>\n'.format(match.highRunW if match.highRunW > 0 else '-'))
                loser = players.Player.get_by_id(match.playerL.id())
                response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(loser.firstName), ref))
                response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(loser.lastName), ref))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.handicapL))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.scoreL))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.targetL))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.highRunL if match.highRunL > 0 else '-'))
            else:
                # For linking to opponent
                ref = '/details/?Season={0}&Player={1}'.format(cgi.escape(season.key.id()), cgi.escape(match.playerW.id()))
                response.write('    <td class="white center">{0}</td>\n'.format('Lost'))
                response.write('    <td class="white center">{0}</td>\n'.format(match.handicapL))
                response.write('    <td class="white center">{0}</td>\n'.format(match.scoreL))
                response.write('    <td class="white center">{0}</td>\n'.format(match.targetL))
                response.write('    <td class="white center">{0}</td>\n'.format(match.highRunL if match.highRunL > 0 else '-'))
                winner = players.Player.get_by_id(match.playerW.id())
                response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(winner.firstName), ref))
                response.write('    <td class="gray left"><a href="{1}">{0}</a></td>\n'.format(cgi.escape(winner.lastName), ref))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.handicapW))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.scoreW))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.targetW))
                response.write('    <td class="gray center">{0}</td>\n'.format(match.highRunW if match.highRunW > 0 else '-'))
            response.write('  </tr>\n')
        response.write('</tbody></table>\n')

        stat = stats.PlayerSummary.query(ndb.AND(stats.PlayerSummary.player == player.key, stats.PlayerSummary.season == season.key)).fetch(1)[0]
        response.write('<p>Wins={0}, Losses={1}\n'.format(stat.wins, stat.losses))
        response.write('<br/>High Run={0}, Target={1}\n'.format(stat.highRun, stat.highRunTarget))
        response.write('<br/><a href="/">Home</a>\n')
        response.write('</center>\n')
        response.write('</br>\n')
