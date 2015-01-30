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
import webapp2

from data import seasons
from data import stats
from data import clubs

TEMPLATE = 'html/add_season.html'

class AddSeasonHandler(base_handler.BaseHandler):
    def post(self, clubid):
        season_code = clubid+'-'+self.request.get('name').replace(' ','-')
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return

        user = users.get_current_user()
        if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        context = {
                'club': club,
                'season_code': season_code,
                'season_name': self.request.get('name'),
                'season_start': self.request.get('start'),
                'season_end': self.request.get('end'),
                }
        error_messages = []

        season = seasons.Season.get_by_id(season_code)
        if season:
            error_messages.append("Duplicate season name (id=%s, club=%s, name=%s)" %
                    (season_code, club.name, context['season_name']))

        try:
            s_start = datetime.datetime.strptime(context['season_start'], "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid start date: %s (%s)\n" %
                    (context['season_start'], err))

        err = None
        try:
            s_end = datetime.datetime.strptime(context['season_end'], "%Y-%m-%d")
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
            season.name = context['season_name']
            season.startDate = datetime.datetime.strptime(context['season_start'], "%Y-%m-%d")
            season.endDate = datetime.datetime.strptime(context['season_end'], "%Y-%m-%d")
            season.club = club.key
            season = season.put()
        self.render_response(TEMPLATE, **context)
        if context['season_code'] == 'lifetime':
            # One shot code to back update the lifetime stats from before the feature was added
            s_list = stats.PlayerSummary.query().order(stats.PlayerSummary.player).fetch()
            lifetime = None
            for stat in s_list:
                if lifetime and lifetime.player != stat.player:
                    lifetime.put()

                if lifetime == None or lifetime.player != stat.player:
                    lifetime = stats.PlayerSummary()
                    lifetime.player = stat.player
                    lifetime.season = season
                    lifetime.wins = 0
                    lifetime.forfeits = 0
                    lifetime.losses = 0
                    lifetime.highRun = 0

                # Update win / loss totals
                lifetime.wins = lifetime.wins + stat.wins
                lifetime.forfeits = lifetime.forfeits + stat.forfeits
                lifetime.losses = lifetime.forfeits + stat.losses
                if lifetime.handicap < stat.handicap:
                    lifetime.handicap = stat.handicap
                if lifetime.highRun < stat.highRun:
                    lifetime.highRun = stat.highRun
                if lifetime.highRunTarget < stat.highRunTarget:
                    lifetime.highRunTarget = stat.highRunTarget
            # Put last players stats.
            lifetime.put()

    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return

        user = users.get_current_user()
        if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
            self.response.clear()
            self.response.set_status(405)
            self.response.out.write("Not authorized")
            return
        if user not in club.owners:
            club.owners.append(user)
            club = club.put()
        context = {
                'season_code': "",
                'season_name': "",
                'club': club,
                'display_form': True,
                }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AddSeasonHandler)],
    debug=True,
    config=base_handler.CONFIG)
