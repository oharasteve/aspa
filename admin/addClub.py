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
import webapp2

from data import clubs
from data import seasons

TEMPLATE = 'html/add_club.html'

class AddClubHandler(base_handler.BaseHandler):
    def post(self):
        context = {
                'club_code': self.request.get('code'),
                'club_name': self.request.get('name'),
                'club_phone': self.request.get('phone'),
                }
        error_messages = []
        club = clubs.Club.get_by_id(context['club_code'])
        if club:
            error_messages.append("Duplicate club (id=%s, name=%s)" %
                    (context['club_code'], context['club_name']))

        if len(error_messages) > 0:
            context['error_messages'] = error_messages
        else:
            club = clubs.Club(key=ndb.Key(clubs.Club, context['club_code']))
            club.name = context['club_name']
            club.phone = context['club_phone']
            club.put()
        self.render_response(TEMPLATE, **context)

    def get(self):
        context = {
                'club_code': "",
                'club_name': "",
                'club_phone': "",

                'display_form': True,
                }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddClubHandler)],
    debug=True,
    config=base_handler.CONFIG)
