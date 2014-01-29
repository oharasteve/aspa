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
import datetime
import webapp2

import seasons

class AddSeasonHandler(webapp2.RequestHandler):
    def post(self):
        season_code = self.request.get('code')
        season_name = self.request.get('name')
        season_start = self.request.get('start')
        season_end = self.request.get('end')

        self.header(self.response)
        errmsg = ""
        if len(season_code) == 0:
            errmsg += "<li>Season code is required\n"
        else:
            season = seasons.Season.get_by_id(season_code)
            if season:
                errmsg += "<li>Duplicate season name (%s)\n" % cgi.escape(season_code)
        if len(season_name) == 0:
            errmsg += "<li>Season name is required\n"

        try:
            sstart = datetime.datetime.strptime(season_start, "%Y-%m-%d")
        except ValueError as err:
            errmsg += "<li>Invalid start date: %s (%s)\n" % (cgi.escape(season_start), err)

        try:
            send = datetime.datetime.strptime(season_end, "%Y-%m-%d")
        except ValueError as err:
            errmsg += "<li>Invalid end date: %s (%s)\n" % (cgi.escape(season_end), err)
        if not errmsg and send < sstart:
            errmsg += "<li>Start date (%s) must precede end date (%s)\n" % (sstart, send)

        if errmsg:
            self.response.write("<h3><font color=red>Errors:<ul>%s</ul></font></h3>\n" % errmsg)
            self.shared(self.response, season_code, season_name, season_start, season_end)
        else:
            season = seasons.Season(key=ndb.Key(seasons.Season,season_code))
            season.name = season_name
            season.startDate = sstart
            season.endDate = send
            season.put()
            self.response.write('<h3>Successfully added new Season: %s (%s)</h3>\n' % (cgi.escape(season_name), cgi.escape(season_code)))
            self.response.write('<p><input type="button" value="Done" onclick="window.location=\'/admin\'">\n')
        self.footer(self.response)

    def get(self):
        self.header(self.response)
        self.shared(self.response, "", "", "", "")
        self.footer(self.response)


    def header(self, response):
        response.write('<html>\n')
        response.write('<head>\n')
        response.write('<title>ASPA</title>\n')
        response.write('</head>\n')
        response.write('<body>\n')

    def shared(self, response, season_code, season_name, season_start, season_end):
        response.write('<h3>Add a New Season</h3>\n')
        response.write('<hr/><form action="/admin/addSeason/" method="post">\n')
        response.write('<table>\n')
        response.write('  <tr>\n')
        response.write('    <td align="right">Code:\n')
        response.write('    <td align="left"><input name="code" size="5" type="text" value="%s">\n' % cgi.escape(season_code))
        response.write('  <tr>\n')
        response.write('    <td align="right">Name:\n')
        response.write('    <td align="left"><input name="name" type="text" value="%s">\n' % cgi.escape(season_name))
        response.write('  <tr>\n')
        response.write('    <td align="right">Start Date:<br>(yyyy-mm-dd)\n')
        response.write('    <td align="left"><input name="start" type="text" value="%s">\n' % cgi.escape(season_start))
        response.write('  <tr>\n')
        response.write('    <td align="right">End Date:<br>(yyyy-mm-dd)\n')
        response.write('    <td align="left"><input name="end" type="text" value="%s">\n' % cgi.escape(season_end))
        response.write('</table>\n')
        response.write('<p>\n')
        response.write('  <input type="button" value="Cancel" onclick="window.location=\'/admin\'">\n')
        response.write('  <input type="submit" value="Submit">\n')
        response.write('</form>\n')

    def footer(self, response):
        response.write('</body>\n')
        response.write('</html>\n')

app = webapp2.WSGIApplication([
  (r'/.*', AddSeasonHandler)
], debug=True)
