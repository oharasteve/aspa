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
from google.appengine.ext import ndb
import cgi
import webapp2

import highRun
import players
import seasons
import stats

class AddPersonHandler(webapp2.RequestHandler):
    def post(self):
        season = seasons.Season.get_by_id('Spr14')
        player_code = self.request.get('code')
        player_first = self.request.get('first')
        player_last = self.request.get('last')
        player_hcap = self.request.get('handicap')
        player_hrun = self.request.get('highRunTarget')
        player_phone = self.request.get('phone')

        self.header(self.response, season)
        errmsg = ""
        if len(player_code) == 0:
            errmsg += "<li>Player code is required\n"
        else:
            player = players.Player.get_by_id(player_code)
            if player:
                errmsg += "<li>Duplicate player (%s)\n" % cgi.escape(player_code)
        if len(player_first) == 0:
            errmsg += "<li>First name is required\n"
        if len(player_last) == 0:
            errmsg += "<li>Last name is required\n"

        if len(player_hcap) == 0:
            errmsg += "<li>Handicap is required\n"
        else:
            try:
                hcap = int(player_hcap)
            except ValueError as err:
                errmsg += "<li>Invalid handicap: %s (%s)\n" % (cgi.escape(player_hcap), err)

        if len(player_hrun) == 0:
            errmsg += "<li>High run target is required\n"
        else:
            try:
                hrun = float(player_hrun)
            except ValueError as err:
                errmsg += "<li>Invalid high run target: %s (%s)\n" % (cgi.escape(player_hrun), err)

        if errmsg:
            self.response.write("<h3><font color=red>Errors:<ul>%s</ul></font></h3>\n" % errmsg)
            self.shared(self.response, player_code, player_first, player_last, player_hcap, player_hrun, player_phone)
        else:
            player = players.Player(key=ndb.Key(players.Player,player_code))
            player.firstName = player_first
            player.lastName = player_last
            player.phone = player_phone
            player.put()

            stat = stats.PlayerSummary(key=ndb.Key(stats.PlayerSummary,player_code))
            stat.player = player.key
            stat.season = season.key
            stat.handicap = hcap
            stat.highRunTarget = hrun
            stat.highRun = 0
            stat.wins = 0
            stat.losses = 0
            stat.put()

            self.response.write('<h3>Successfully added new Player: %s %s (%s)</h3>\n' % (cgi.escape(player_first), cgi.escape(player_last), cgi.escape(player_code)))
            self.response.write('<p><input type="button" value="Done" onclick="window.location=\'/admin\'">\n')
        self.footer(self.response)

    def get(self):
        season = seasons.Season.get_by_id('Spr14')
        self.header(self.response, season)
        self.shared(self.response, "", "", "", "", "", "")
        self.footer(self.response)


    def header(self, response, season):
        response.write('<html>\n')
        response.write('<head>\n')
        response.write('<title>ASPA {0}</title>\n'.format(cgi.escape(season.name)))
        response.write('<script language="javascript">\n')
        highRun.insertJavascript(self.response)
        response.write('</script>\n')
        response.write('</head>\n')
        response.write('<body>\n')

    def shared(self, response, player_code, player_first, player_last, player_hcap, player_hrun, player_phone):
        response.write('<h3>Add a New Player</h3>\n')
        response.write('<hr/><form action="/admin/addPlayer/" method="post">\n')
        response.write('<table>\n')
        response.write('  <tr>\n')
        response.write('    <td align="right">Code:\n')
        response.write('    <td align="left"><input name="code" size="5" type="text" value="%s">\n' % cgi.escape(player_code))
        response.write('  <tr>\n')
        response.write('    <td align="right">First Name:\n')
        response.write('    <td align="left"><input name="first" type="text" value="%s">\n' % cgi.escape(player_first))
        response.write('  <tr>\n')
        response.write('    <td align="right">Last Name:\n')
        response.write('    <td align="left"><input name="last" type="text" value="%s">\n' % cgi.escape(player_last))
        response.write('  <tr>\n')
        response.write('    <td align="right">Handicap:\n')
        response.write('    <td align="left"><input size="5" onchange=\'highRun("handicap","highRunTarget")\' id="handicap" name="handicap" type="text" value="%s">\n' % cgi.escape(player_hcap))
        response.write('  <tr>\n')
        response.write('    <td align="right">High Run Target:\n')
        response.write('    <td align="left"><input size="5" id="highRunTarget" name="highRunTarget" type="text" value="%s">\n' % cgi.escape(player_hrun))
        response.write('  <tr>\n')
        response.write('    <td align="right">Phone:\n')
        response.write('    <td align="left"><input name="phone" type="text" value="%s">\n' % cgi.escape(player_phone))
        response.write('</table>\n')
        response.write('<p>\n')
        response.write('  <input type="button" value="Cancel" onclick="window.location=\'/admin\'">\n')
        response.write('  <input type="submit" value="Submit">\n')
        response.write('</form>\n')

    def footer(self, response):
        response.write('</body>\n')
        response.write('</html>\n')

app = webapp2.WSGIApplication([
  (r'/.*', AddPersonHandler)
], debug=True)
