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

TEMPLATE = 'html/delete_match.html'

class DeleteMatchHandler(base_handler.BaseHandler):
    def post(self):
        xseason = self.request.get('season_select')
        xseq = self.request.get('seq')
        xclub = self.request.get('club_select')
        xwhen = self.request.get('match_date')
        nameW = self.request.get('winner_select')
        nameL = self.request.get('loser_select')

        successfully_deleted_match = False
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

        seq = int(xseq)
        if not seq:
            error_messages.append("Sequence number is required")

        if not len(error_messages):
            matchList = matches.Match.query(
                ndb.AND(matches.Match.playerW == winner.key,
                    matches.Match.playerL == loser.key,
                    matches.Match.season == season.key,
                    matches.Match.club == club.key,
                    matches.Match.seq == seq,
                    matches.Match.date == when)).fetch(1)
            if not matchList:
                error_messages.append("Unable to find the match between %s and %s (%s at %s, #%d on %s)" %
                    (winner.key.id(), loser.key.id(), season.key.id(), club.key.id(), seq, when.strftime('%b %d, %Y')))
            else:
                match = matchList[0]
                logging.info("Deleting match between %s and %s (%s at %s, #%d on %s)" %
                    (match.playerW.id(), match.playerL.id(), match.season.id(), match.club.id(), match.seq or 0, match.date.strftime('%b %d, %Y')))

                # Delete the match
                ndb.Key(matches.Match, match.key.id()).delete()

                stats.removeMatch(season.key, match.playerW, 1)
                # TODO: Deal with undoing a forefit?
                stats.removeMatch(season.key, match.playerL, 0)

                successfully_deleted_match = True

        context = {
          'seasons': seasons.Season.getSeasons(),
          'match_date': xwhen,
          'seq': xseq,
          'players': players.Player.getPlayers(),
          'clubs': clubs.Club.getClubs(),
          'club': club,
          'winner': {
              'firstName': winner.firstName,
              'lastName': winner.lastName,
              'player_id': nameW,
              },
          'loser': {
              'firstName': loser.firstName,
              'lastName': loser.lastName,
              'player_id': nameL,
              },
          'season_selected': xseason,
          'club_selected': xclub,
          'winner_selected': nameW,
          'loser_selected': nameL,
          'display_form': True,
          'successfully_deleted_match': successfully_deleted_match,
          'error_messages': error_messages,
        }

        self.render_response(TEMPLATE, **context)

    def get(self):
        season = seasons.Season.query().order(-seasons.Season.endDate).get();
        currDate = datetime.date.today()
        weekDay = currDate.weekday()      # 0=Mon ... 6=Sun
        adjustDays = (weekDay + 6) % 7    # 6=Mon ... 5=Sun
        matchDate = currDate - datetime.timedelta(days=adjustDays)
        context = {
          'seasons': seasons.Season.getSeasons(),
          'match_date': matchDate.strftime('%Y-%m-%d'),
          'seq': 0,
          'players': players.Player.getPlayers(),
          'clubs': clubs.Club.getClubs(),
          'winner': {
              'player_id': '',
              },
          'loser': {
              'player_id': '',
              },
          'season_selected': season.key,
          'club_selected': 'LS',
          'winner_selected': -1,
          'loser_selected': -1,
          'display_form': True,
        }
        logging.info('playerStats size = %d for %s' % (len(stats.PlayerSummary.getPlayerSummaries(season)), season.name))
        self.render_response(TEMPLATE, **context)


app = webapp2.WSGIApplication([(r'/.*', DeleteMatchHandler)],
    debug=True,
    config=base_handler.CONFIG)
