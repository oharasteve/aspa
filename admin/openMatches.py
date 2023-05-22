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
import json
import logging
import webapp2

from data import clubs
from data import matches
from data import players
from data import seasons
from data import stats

TEMPLATE = 'html/open_matches.html'

class OpenMatchesHandler(base_handler.BaseHandler):


    def post(self, clubid):
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

        lifetime = seasons.Season.get_by_id('lifetime')
        match_key = self.request.get('match_id')
        xwhen = self.request.get('date')
        nameA = self.request.get('a_id')
        nameB = self.request.get('b_id')
        xtargetA = self.request.get('a_target')
        xtargetB = self.request.get('b_target')
        xscoreA = self.request.get('a_score')
        xscoreB = self.request.get('b_score')
        xhrunA = self.request.get('a_highrun')
        xhrunB = self.request.get('b_highrun')

        match = matches.Match.get_by_id(int(match_key))

        if xwhen is '':
            match.key.delete()
            self.response.clear()
            self.response.set_status(200)
            return

        # backdate to league night
        season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.endDate).get();
        currDate = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        weekDay = currDate.weekday()               # 0=Mon ... 6=Sun
        seasonDay = season.startDate.weekday()     # 0=Mon ... 6=Sun
        adjustDays = (weekDay + 7-seasonDay) % 7   # 6=Mon ... 5=Sun for seasonDay == Tue
        matchDate = currDate - datetime.timedelta(days=adjustDays)
        xwhen = matchDate.strftime('%Y-%m-%d')

        nameW = nameA
        nameL = nameB

        targetA = int(xtargetA) if xtargetA else None
        targetB = int(xtargetB) if xtargetB else None
        scoreA = int(xscoreA) if xscoreA else None
        scoreB = int(xscoreB) if xscoreB else None
        hrunA = int(xhrunA) if xhrunA else None
        hrunB = int(xhrunB) if xhrunB else None

        targetW = targetA
        targetL = targetB
        scoreW = scoreA
        scoreL = scoreB
        hrunW = hrunA
        hrunL = hrunB

        winner = players.Player.get_by_id(nameW)
        loser = players.Player.get_by_id(nameL)

        if targetW != scoreW:
            targetW = targetB
            targetL = targetA
            scoreW = scoreB
            scoreL = scoreA
            hrunW = hrunB
            hrunL = hrunA
            winner,loser = loser,winner
            # Now fix up the match record fields
            match.playerW, match.playerL = match.playerL, match.playerW
            match.handicapW, match.handicapL = match.handicapL, match.handicapW

        successfully_added_match = False
        error_messages = []

        if not winner:
            error_messages.append("Winner is required")

        if not loser:
            error_messages.append("Loser is required")

        if scoreW is not None:
            if scoreW != targetW:
              error_messages.append("Winner score (%s) does not match target (%s)\n" % (scoreW, match.targetW))
            if scoreL >= targetL:
              error_messages.append("Loser score (%s) is too high (%s)\n" % (scoreL, match.targetL))

        if not len(error_messages):
            if scoreW and match.season not in winner.seasons:
                for (season_idx, season_rec) in enumerate(winner.seasons):
                    if season_rec.get().club == club.key:
                        del winner.seasons[season_idx]
                        break
                winner.seasons.append(match.season)
                winner.put()
            if scoreL and match.season not in loser.seasons:
                for (season_idx, season_rec) in enumerate(loser.seasons):
                    if season_rec.get().club == club.key:
                        del loser.seasons[season_idx]
                        break
                loser.seasons.append(match.season)
                loser.put()

            # update record match
            match.seq = 1 # TODO(snoonan) 21.12 Make this useful again

            match.targetW = targetW
            match.scoreW = scoreW
            match.highRunW = hrunW

            match.targetL = targetL
            match.scoreL = scoreL
            match.highRunL = hrunL

            match.put()

            # Update statistics for the winner and loser
            stats.addMatch(match.season, winner.key, 1, match.handicapW, match.scoreW, match.highRunW)
            stats.addMatch(match.season, loser.key, 0, match.handicapL, match.scoreL, match.highRunL)
            if lifetime:
                stats.addMatch(lifetime.key, winner.key, 1, match.handicapW, match.scoreW, match.highRunW)
                stats.addMatch(lifetime.key, loser.key, 0, match.handicapL, match.scoreL, match.highRunL)

            successfully_added_match = True

        context = {}
        context['successfully_added_match'] = successfully_added_match
        context['error_messages'] = error_messages
        self.response.clear()
        self.response.set_status(200)
        self.response.out.write(json.dumps(context))

    def get(self, clubid):
        club = clubs.Club.get_by_id(clubid)
        if club == None:
           clubs.sendNoSuch(clubid)
           return
        user = users.get_current_user()
        authorized = True
        if user not in club.owners and user.email().lower() not in club.invited and not users.is_current_user_admin():
            authorized = False
            #self.response.clear()
            #self.response.set_status(405)
            #self.response.out.write("Not authorized")
            #return
        if authorized and user not in club.owners:
            club.owners.append(user)
            club = club.put()
        season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.endDate).get();

        open_matches = matches.Match.query(
            matches.Match.season == season.key, matches.Match.scoreW == None)

        open_match_context = [ {
          'date': m.date.strftime('%Y-%m-%d'),
          'key': m.key.id(),
          'playera': {
              'id': m.playerW.id(),
              'name': m.playerW.get().firstName+" "+m.playerW.get().lastName,
              'target': m.targetW,
              },
          'playerb': {
              'id': m.playerL.id(),
              'name': m.playerL.get().firstName+" "+m.playerL.get().lastName,
              'target': m.targetL,
              },
            } for m in open_matches]

        context = {
          'season': season,
          'club': club,
          'matches': open_match_context,
          'display_form': True,
          'admin': authorized,
          }

        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', OpenMatchesHandler)],
    debug=True,
    config=base_handler.CONFIG)
