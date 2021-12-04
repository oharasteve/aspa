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
from google.appengine.api import users

import base_handler
import webapp2

from data import seasons
from data import clubs

TEMPLATE = 'html/admin.html'

class AdminHandler(base_handler.BaseHandler):
    def get(self, clubid):
        user = users.get_current_user()
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           if not users.is_current_user_admin():
               self.response.clear()
               self.response.set_status(405)
               self.response.out.write("Not authorized")
               return
           context = {
            'season': {'name':""},
            'club': {'key': {'id':lambda: ""}},
            'choices': [
                {
                    'url': '/%s/admin/addPhoto/'%(clubid,),
                    'description': 'Add a Photo',
                    'help': 'one photo per person',
                },
                {
                    'url': '/admin/addClub/',
                    'description': 'Add New Club',
                    'help': 'not needed yet',
                },
            ],
           }
           self.render_response(TEMPLATE, **context)
           return
        user = users.get_current_user()
        if user not in club.owners and user.email().lower() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        season = seasons.Season.query().order(-seasons.Season.endDate);
        if not season:
            season = {'name':""}
        context = {
            'season': season,
            'club': club,
            'choices': [
                {
                    'url': '/%s/admin/suggestMatch/'%(clubid,),
                    'description': 'Suggest Match Targets',
                    'help': 'help choose race',
                },
                {
                    'url': '/%s/admin/openMatches/'%(clubid,),
                    'description': 'List of open matches to fill in scores',
                    'help': 'fill out open matches',
                },
                {
                    'url': '/%s/admin/addMatch/'%(clubid,),
                    'description': 'Add Match Results',
                    'help': 'once a week',
                },
                {
                    'url': '/%s/admin/saveResults/'%(clubid,),
                    'description': 'Upload Weekly Results',
                    'help': 'once a week',
                },
                {
                    'url': '/%s/admin/addPlayer/'%(clubid,),
                    'description': 'Add New Player',
                    'help': 'brand new players only',
                },
                {
                    'url': '/%s/admin/editPlayer/'%(clubid,),
                    'description': 'Edit Player',
                    'help': 'update email or fix name',
                },
                {
                    'url': '/%s/admin/addVideo/'%(clubid,),
                    'description': 'Add a Video',
                    'help': 'from YouTube',
                },
                {
                    'url': '/%s/admin/addPhoto/'%(clubid,),
                    'description': 'Add a Photo',
                    'help': 'one photo per person',
                },
                {
                    'url': '/%s/admin/addSeason/'%(clubid,),
                    'description': 'Add New Season',
                    'help': 'once per season',
                },
                {
                    'url': '/%s/admin/addSeasonResult/'%(clubid,),
                    'description': 'Add Season Result',
                    'help': 'season totals from a previous season',
                },
                {
                    'url': '/%s/admin/addClub/'%(clubid,),
                    'description': 'Edit Club',
                    'help': 'not needed yet',
                },
                {
                    'url': '/%s/admin/adjustHandicap/'%(clubid,),
                    'description': 'Adjust Player Handicap',
                    'help': 'League Manager only',
                },
                {
                    'url': '/%s/admin/deleteMatch/'%(clubid,),
                    'description': 'Delete Match Result',
                    'help': 'Rarely needed (hopefully)',
                },
                {
                    'url': '/%s/admin/carryPlayer/'%(clubid,),
                    'description': 'Carry Player Forward',
                    'help': 'from previous season',
                },
            ],
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AdminHandler)],
    debug=True,
    config=base_handler.CONFIG)
