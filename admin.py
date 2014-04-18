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
        context = {
                'season': seasons.Season.get_by_id('Spr14'),
                'choices': [
                    {
                        'url': '/admin/suggestMatch/',
                        'description': 'Suggest Match Targets',
                        },
                    {
                        'url': '/admin/addMatch/',
                        'description': 'Add Match Result',
                        },
                    {
                        'url': '/admin/addPlayer/',
                        'description': 'Add New Player',
                        },
                    {
                        'url': '/admin/addSeason/',
                        'description': 'Add New Season',
                        },
                    {
                        'url': '/admin/addSeasonResult/',
                        'description': 'Add Season Result',
                        },
                    {
                        'url': '/admin/addClub/',
                        'description': 'Add New Club',
                        },
                    {
                        'url': '/admin/adjustHandicap/',
                        'description': 'Adjust Player Handicap',
                        },
                    ],
                }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AdminHandler)],
    debug=True,
    config=base_handler.CONFIG)
