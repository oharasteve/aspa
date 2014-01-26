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

import clubs
import seasons

class AddClubHandler(webapp2.RequestHandler):
  def post(self):
    club_code = self.request.get('code')
    club_name = self.request.get('name')
    club_phone = self.request.get('phone')
    
    self.header(self.response)
    errmsg = ""
    if len(club_code) == 0:
      errmsg += "<li>Club code is required\n"
    else:
      club = clubs.Club.get_by_id(club_code)
      if club:
        errmsg += "<li>Duplicate club name (%s)\n" % cgi.escape(club_code)
    if len(club_name) == 0:
      errmsg += "<li>Club name is required\n"

    if errmsg:
      self.response.write("<h3><font color=red>Errors:<ul>%s</ul></font></h3>\n" % errmsg)
      self.shared(self.response, club_code, club_name, club_phone)
    else:
      club = clubs.Club(key=ndb.Key(clubs.Club,club_code))
      club.name = club_name
      club.phone = club_phone
      club.put()
      self.response.write('<h3>Successfully added new Club: %s (%s)</h3>\n' % (cgi.escape(club_name), cgi.escape(club_code)))
      self.response.write('<p><input type="button" value="Done" onclick="window.location=\'/admin\'">\n')
    self.footer(self.response)
  
  def get(self):
    self.header(self.response)
    self.shared(self.response, "", "", "")
    self.footer(self.response)
    

  def header(self, response):
    season = seasons.Season.get_by_id('Spr14')
    response.write('<html>\n')
    response.write('<head>\n')
    response.write('<title>ASPA {0}</title>\n'.format(cgi.escape(season.name)))
    response.write('</head>\n')
    response.write('<body>\n')
    
  def shared(self, response, club_code, club_name, club_phone):
    response.write('<h3>Add a New Club</h3>\n')
    response.write('<hr/><form action="/admin/addClub/" method="post">\n')
    response.write('<table>\n')
    response.write('  <tr>\n')
    response.write('    <td align="right">Code:\n')
    response.write('    <td align="left"><input name="code" size="5" type="text" value="%s">\n' % cgi.escape(club_code))
    response.write('  <tr>\n')
    response.write('    <td align="right">Name:\n')
    response.write('    <td align="left"><input name="name" type="text" value="%s">\n' % cgi.escape(club_name))
    response.write('  <tr>\n')
    response.write('    <td align="right">Phone:\n')
    response.write('    <td align="left"><input name="phone" type="text" value="%s">\n' % cgi.escape(club_phone))
    response.write('</table>\n')
    response.write('<p>\n')
    response.write('  <input type="button" value="Cancel" onclick="window.location=\'/admin\'">\n')
    response.write('  <input type="submit" value="Submit">\n')
    response.write('</form>\n')

  def footer(self, response):
    response.write('</body>\n')
    response.write('</html>\n')
      
app = webapp2.WSGIApplication([
  (r'/.*', AddClubHandler)
], debug=True)
