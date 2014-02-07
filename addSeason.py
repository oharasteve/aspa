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
import base_handler
import cgi
import datetime
import webapp2

from data import seasons

TEMPLATE = 'html/add_season.html'

class AddSeasonHandler(base_handler.BaseHandler):
    def post(self):
        context = {
                'season_code': self.request.get('code'),
                'season_name': self.request.get('name'),
                'season_start': self.request.get('start'),
                'season_end': self.request.get('end'),
                }
        error_messages = []

        season = seasons.Season.get_by_id(context['season_code'])
        if season:
            error_messages.append("Duplicate season name (id=%s, code=%s)" %
                    (context['season_code'], context['season_name']))

        try:
            s_start = datetime.datetime.strptime(context['season_start'], "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid start date: %s (%s)\n" %
                    (context['season_start'], err))

        try:
            s_end = datetime.datetime.strptime(season_end, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid end date: %s (%s)\n" %
                    (context['season_end'], err))
        if not err and s_end < s_start:
            error_messages.append(
                    "Start date (%s) must precede end date (%s)\n" % (s_start,
                        s_end))

        if len(error_messages):
            context['error_messages'] = error_messages
        else:
            season = seasons.Season(key=ndb.Key(seasons.Season,season_code))
            season.name = season_name
            season.startDate = sstart
            season.endDate = send
            season.put()
        self.render_response(TEMPLATE, **context)

    def get(self):
        context = {
                'season_code': "",
                'season_name': "",
                'season_phone': "",

                'display_form': True,
                }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddSeasonHandler)],
    debug=True,
    config=base_handler.CONFIG)
