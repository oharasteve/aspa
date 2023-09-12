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

import base_handler
import cgi
import datetime
import logging
import webapp2

from data import clubs
from data import matches
from data import players
from data import seasons
from data import stats

class StartMatchHandler(base_handler.BaseHandler):

    def post(self, clubid):
        error_messages = []

        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
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
        match_key = self.request.get('match_id')
        xseason = self.request.get('season_select')
        xwhen = self.request.get('match_date')
        nameA = self.request.get('playera_select')
        nameB = self.request.get('playerb_select')
        xhcapA = self.request.get('playera_handicap')
        xhcapB = self.request.get('playerb_handicap')
        xtargetA = self.request.get('playera_target')
        xtargetB = self.request.get('playerb_target')

        if not nameA:
            error_messages.append("PlayerA is required")

        if not nameB:
            error_messages.append("PlayerB is required")

        if not xseason:
            error_messages.append("Season is required")

        if len(error_messages):
            self.response.clear()
            self.response.set_status(400)
            self.response.out.write(error_messages)

        nameW = nameA
        nameL = nameB

        hcapA = int(xhcapA)
        hcapB = int(xhcapB)
        targetA = int(xtargetA)
        targetB = int(xtargetB)

        hcapW = hcapA
        hcapL = hcapB
        targetW = targetA
        targetL = targetB

        winner = players.Player.get_by_id(nameW)
        loser = players.Player.get_by_id(nameL)
        season = seasons.Season.get_by_id(xseason)

        try:
            when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid date: %s (%s)" % (cgi.escape(xwhen), err))

        if not winner:
            error_messages.append("PlayerA is required")

        if not loser:
            error_messages.append("PlayerB is required")

        if not season:
            error_messages.append("Season is required")

        if len(error_messages):
            self.response.clear()
            self.response.set_status(400)
            self.response.out.write(error_messages)

        if not len(error_messages):
            # record match
            match = matches.Match()
            match.date = when
            match.season = season.key
            match.club = club.key

            match.playerW = winner.key
            match.handicapW = hcapW
            match.targetW = targetW

            match.playerL = loser.key
            match.handicapL = hcapL
            match.targetL = targetL

            match.put()

            self.response.clear()
            self.response.set_status(200)
            self.response.out.write("")

app = webapp2.WSGIApplication([(r'/([^/]*)/.*', StartMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
