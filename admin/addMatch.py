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

TEMPLATE = 'html/add_match.html'

class AddMatchHandler(base_handler.BaseHandler):
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
        xseason = self.request.get('season_select')
        xseq = self.request.get('seq')
        xwhen = self.request.get('match_date')
        nameA = self.request.get('playera_select')
        nameB = self.request.get('playerb_select')
        xhcapA = self.request.get('playera_handicap')
        xhcapB = self.request.get('playerb_handicap')
        xtargetA = self.request.get('playera_target')
        xtargetB = self.request.get('playerb_target')
        xscoreA = self.request.get('playera_score')
        xscoreB = self.request.get('playerb_score')
        xhrunA = self.request.get('playera_highrun')
        xhrunB = self.request.get('playerb_highrun')
        forfeit = (self.request.get('forfeit') == 'on')

        nameW = nameA
        nameL = nameB

        seq = int(xseq)
        hcapA = int(xhcapA)
        hcapB = int(xhcapB)
        targetA = int(xtargetA)
        targetB = int(xtargetB)
        scoreA = int(xscoreA)
        scoreB = int(xscoreB)
        hrunA = int(xhrunA)
        hrunB = int(xhrunB)

        hcapW = hcapA
        hcapL = hcapB
        targetW = targetA
        targetL = targetB
        scoreW = scoreA
        scoreL = scoreB
        hrunW = hrunA
        hrunL = hrunB

        winner = players.Player.get_by_id(nameW)
        loser = players.Player.get_by_id(nameL)
        season = seasons.Season.get_by_id(xseason)

        context = {
          'seasons': seasons.Season.getSeasons(club),
          'match_date': xwhen,
          'seq': seq,
          'players': stats.PlayerSummary.getPlayers(season),
          'playerStats': stats.PlayerSummary.getPlayerSummaries(season),
          'club': club,
          'playera': {
              'firstName': winner.firstName,
              'lastName': winner.lastName,
              'player_id': nameA,
              'handicap': xhcapA,
              'target': xtargetA,
              'highrun': xhrunA,
              'score': xscoreA,
              },
          'playerb': {
              'firstName': loser.firstName,
              'lastName': loser.lastName,
              'player_id': nameB,
              'handicap': xhcapB,
              'target': xtargetB,
              'highrun': xhrunB,
              'score': xscoreB,
              },
          'forfeit': forfeit,
          'season_selected': xseason,
          'club_selected': club,
          'playera_selected': nameW,
          'playerb_selected': nameL,
          'display_form': True,
        }

        if int(xtargetA) != int(xscoreA):
            nameW = nameB
            nameL = nameA
            hcapW = hcapB
            hcapL = hcapA
            targetW = targetB
            targetL = targetA
            scoreW = scoreB
            scoreL = scoreA
            hrunW = hrunB
            hrunL = hrunA
            winner,loser = loser,winner

        successfully_added_match = False
        error_messages = []
        try:
            when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid date: %s (%s)" % (cgi.escape(xwhen), err))

        if not winner:
            error_messages.append("Winner is required")

        if not loser:
            error_messages.append("Loser is required")

        if not season:
            error_messages.append("Season is required")


        if not forfeit and scoreW != targetW:
          error_messages.append("Winner score (%s) does not match target (%s)\n" % (scoreW, targetW))
        if scoreL >= targetL:
          error_messages.append("Loser score (%s) is too high (%s)\n" % (scoreL, targetL))

        if not len(error_messages):
            # Setup context for new match
            context['seq'] = context['seq']+1
            context['playera']['highrun'] = 0
            context['playerb']['highrun'] = 0
            context['playera_selected'] = 0
            context['playerb_selected'] = 0

            # record match
            match = matches.Match()
            match.date = when
            match.seq = seq
            match.season = season.key
            match.club = club.key
            match.forfeited = forfeit

            match.playerW = winner.key
            match.handicapW = hcapW
            match.scoreW = scoreW
            match.targetW = targetW
            match.highRunW = hrunW

            match.playerL = loser.key
            match.handicapL = hcapL
            match.scoreL = scoreL
            match.targetL = targetL
            match.highRunL = hrunL

            match.put()

            # Update statistics for the winner and loser
            stats.addMatch(match.season, winner.key, 1, hcapW, scoreW, hrunW)
            if forfeit:
               stats.addMatch(match.season, loser.key, None, hcapL, scoreL, hrunL)
            else:
               stats.addMatch(match.season, loser.key, 0, hcapL, scoreL, hrunL)

            successfully_added_match = True

            # Clear high runs for the next match
            xhrunW = 0
            xhrunL = 0

        context['successfully_added_match'] = successfully_added_match
        context['error_messages'] = error_messages
        self.render_response(TEMPLATE, **context)

    def get(self, clubid):
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
        season = seasons.Season.query(seasons.Season.club == club.key).order(-seasons.Season.endDate).get();
        currDate = datetime.date.today()
        weekDay = currDate.weekday()               # 0=Mon ... 6=Sun
        seasonDay = season.startDate.weekday()         # 0=Mon ... 6=Sun
        adjustDays = (weekDay + 7-seasonDay) % 7   # 6=Mon ... 5=Sun for seasonDay == Tue
        matchDate = currDate - datetime.timedelta(days=adjustDays)
        context = {
          'seasons': seasons.Season.getSeasons(club),
          'match_date': matchDate.strftime('%Y-%m-%d'),
          'seq': 1,
          'players': stats.PlayerSummary.getPlayers(season),
          'playerStats': stats.PlayerSummary.getPlayerSummaries(season),
          'club': club,
          'playera': {
              'player_id': '',
              'handicap': '',
              'target': '',
              'highrun': 0,
              'score': '',
              },
          'playerb': {
              'player_id': '',
              'handicap': '',
              'target': '',
              'highrun': 0,
              'score': '',
              },
          'forfeit': False,
          'season_selected': season.key,
          'club_selected': 'LS',
          'playera_selected': -1,
          'playerb_selected': -1,
          'display_form': True,
        }
        logging.info('playerStats size = %d for %s' % (len(stats.PlayerSummary.getPlayerSummaries(season)), season.name))
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/([^/]*)/.*', AddMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
