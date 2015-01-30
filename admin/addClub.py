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
from google.appengine.api import users

import logging

import base_handler
import cgi
import webapp2

from data import clubs
from data import seasons

TEMPLATE = 'html/add_club.html'

class AddClubHandler(base_handler.BaseHandler):
    def post(self, clubid):
        user = users.get_current_user()
        context = {
                'user': user,
                'club_code': self.request.get('code'),
                'club_name': self.request.get('name'),
                'club_phone': self.request.get('phone'),
                'newowner': self.request.get('owner'),
                }
        remove = self.request.get_all('remove')
        error_messages = []
        club = clubs.Club.get_by_id(context['club_code'])
        if club and user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if club and user not in club.owners:
            club.owners.append(user)
            del club.invited[club.invited.index(user.email())]
            club = club.put().get()
        if not club:
            club = clubs.Club(key=ndb.Key(clubs.Club, context['club_code']))
        if context['newowner']:
           club.invited.append(context['newowner'])
        logging.info(club.owners)
        logging.info(club.invited)
        logging.info("To remove "+str(remove))
        for email in remove:
           if email in club.invited:
               del club.invited[club.invited.index(email)]
           for op in club.owners:
               if email == op.email():
                 del club.owners[club.owners.index(op)]
        logging.info(club.owners)
        logging.info(club.invited)

        club.name = context['club_name']
        club.phone = context['club_phone']
        club = club.put().get()
        context['club'] = club
        self.render_response(TEMPLATE, **context)

    def get(self, clubid):
        user = users.get_current_user()
        club = clubs.Club.get_by_id(clubid)
        if club and user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        context = {}
        if club:
           owners = club.owners
           owners.extend(club.invited)
           context = {
                   'user': user,
                   'club': club,
                   'club_code': club.key.id(),
                   'club_name': club.name,
                   'club_phone': club.phone,
                   'owners': owners,

                   'display_form': True,
                   }
        else:
           context = {
                   'user': user,
                   'club': None,
                   'club_code': "",
                   'club_name': "",
                   'club_phone': "",

                   'display_form': True,
                   }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/(?:([^/]*)/).*', AddClubHandler)],
    debug=True,
    config=base_handler.CONFIG)
