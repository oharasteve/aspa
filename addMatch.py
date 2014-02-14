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
import logging
import webapp2

from data import clubs
from data import matches
from data import players
from data import seasons
from data import stats

TEMPLATE = 'html/add_match.html'

class AddMatchHandler(base_handler.BaseHandler):
    def post(self):
        xseason = self.request.get('season_select')
        xclub = self.request.get('club_select')
        xwhen = self.request.get('todays_date')
        nameW = self.request.get('winner_select')
        nameL = self.request.get('loser_select')
        xhcapW = self.request.get('winner_handicap')
        xhcapL = self.request.get('loser_handicap')
        xtargetW = self.request.get('winner_target')
        xtargetL = self.request.get('loser_target')
        xscoreW = self.request.get('winner_score')
        xscoreL = self.request.get('loser_score')
        xhrunW = self.request.get('winner_highrun')
        xhrunL = self.request.get('loser_highrun')
        forfeit = self.request.get('forfeit')

        error_messages = []
        try:
            when = datetime.datetime.strptime(xwhen, "%Y-%m-%d")
        except ValueError as err:
            error_messages.append("Invalid date: %s (%s)" % (cgi.escape(xwhen), err))

        winner = players.Player.get_by_id(nameW)
        if not winner:
            error_messages.append("Winner is required")

        loser = players.Player.get_by_id(nameL)
        if not loser:
            error_messages.append("Loser is required")

        season = seasons.Season.get_by_id(xseason)
        if not season:
            error_messages.append("Season is required")

        club = clubs.Club.get_by_id(xclub)
        if not club:
            error_messages.append("Club is required")

        hcapW = int(xhcapW)
        hcapL = int(xhcapL)
        targetW = int(xtargetW)
        targetL = int(xtargetL)
        scoreW = int(xscoreW)
        scoreL = int(xscoreL)
        hrunW = int(xhrunW)
        hrunL = int(xhrunL)

        if not forfeit and scoreW != targetW:
          error_messages.append("Winner score (%s) does not match target (%s)\n" % (scoreW, targetW))
        if scoreL >= targetL:
          error_messages.append("Loser score (%s) is too high (%s)\n" % (scoreL, targetL))

        if not len(error_messages):
            match = matches.Match()
            match.date = when
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
            winnerStats = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerW).fetch(1)[0]
            loserStats = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerL).fetch(1)[0]

            # Update win / loss totals
            winnerStats.wins = winnerStats.wins + 1
            if forfeit:
              loserStats.forfeits = loserStats.forfeits + 1
            else:
              loserStats.losses = loserStats.losses + 1

            # Update handicaps
            winnerStats.handicap = winnerStats.handicap + 3
            loserStats.handicap = loserStats.handicap - 3

            # Update high runs
            if hrunW > winnerStats.highRun:
                winnerStats.highRun = hrunW
            if hrunL > loserStats.highRun:
                loserStats.highRun = hrunL

            winnerStats.put()
            loserStats.put()

        context = {
          'seasons': seasons.Season.getSeasons(),
          'todays_date': xwhen,
          'players': players.Player.getPlayers(),
          'player_summaries': stats.PlayerSummary.getPlayerSummaries(),
          'clubs': clubs.Club.getClubs(),
          'club': club,
          'winner': {
              'firstName': winner.firstName,
              'lastName': winner.lastName,
              'player_id': nameW,
              'handicap': xhcapW,
              'target': xtargetW,
              'highrun': xhrunW,
              'score': xscoreW,
              },
          'loser': {
              'firstName': loser.firstName,
              'lastName': loser.lastName,
              'player_id': nameL,
              'handicap': xhcapL,
              'target': xtargetL,
              'highrun': xhrunL,
              'score': xscoreL,
              },
          'forfeit': forfeit,
          'season_selectedIndex': season,
          'club_selectedIndex': club,
          'winner_selectedIndex': nameW,
          'loser_selectedIndex': nameL,
          'display_form': False,  # Do not display the form, just the errors/result.
          'error_messages': error_messages,
        }

        self.render_response(TEMPLATE, **context)

    def get(self):
        context = {
          'seasons': seasons.Season.getSeasons(),
          'todays_date': datetime.date.today().strftime('%Y-%m-%d'),
          'players': players.Player.getPlayers(),
          'player_summaries': stats.PlayerSummary.getPlayerSummaries(),
          'clubs': clubs.Club.getClubs(),
          'winner': {
              'player_id': '',
              'handicap': '',
              'target': '',
              'highrun': 0,
              'score': '',
              },
          'loser': {
              'player_id': '',
              'handicap': '',
              'target': '',
              'highrun': 0,
              'score': '',
              },
          'forfeit': False,
          'season_selectedIndex': 0,
          'club_selectedIndex': 0,
          'winner_selectedIndex': -1,
          'loser_selectedIndex': -1,
          'display_form': True,
        }
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', AddMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
