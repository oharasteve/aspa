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
import base_handler
import webapp2

from data import seasons

TEMPLATE = 'html/admin.html'

class AdminHandler(base_handler.BaseHandler):
    def get(self):
        season = seasons.Season.query().order(-seasons.Season.endDate).get();
        context = {
            'season': season.key,
            'choices': [
                {
                    'url': '/admin/suggestMatch/',
                    'description': 'Suggest Match Targets',
                    'help': 'help choose race',
                },
                {
                    'url': '/admin/addMatch/',
                    'description': 'Add Match Results',
                    'help': 'once a week',
                },
                {
                    'url': '/admin/saveResults/',
                    'description': 'Upload Weekly Results',
                    'help': 'once a week',
                },
                {
                    'url': '/admin/addPlayer/',
                    'description': 'Add New Player',
                    'help': 'brand new players only',
                },
                {
                    'url': '/admin/addVideo/',
                    'description': 'Add a Video',
                    'help': 'from YouTube',
                },
                {
                    'url': '/admin/addSeason/',
                    'description': 'Add New Season',
                    'help': 'once per season',
                },
                {
                    'url': '/admin/addSeasonResult/',
                    'description': 'Add Season Result',
                    'help': 'season totals from a previous season',
                },
                {
                    'url': '/admin/addClub/',
                    'description': 'Add New Club',
                    'help': 'not needed yet',
                },
                {
                    'url': '/admin/adjustHandicap/',
                    'description': 'Adjust Player Handicap',
                    'help': 'League Manager only',
                },
                {
                    'url': '/admin/deleteMatch/',
                    'description': 'Delete Match Result',
                    'help': 'Rarely needed (hopefully)',
                },
                {
                    'url': '/admin/carryPlayer/',
                    'description': 'Carry Player Forward',
                    'help': 'from previous season',
                },
            ],
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AdminHandler)],
    debug=True,
    config=base_handler.CONFIG)
