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
import webapp2
from google.appengine.ext import ndb
import datetime
import logging

import clubs
import highRun
import matches
import players
import seasons
import stats

class FakeHandler(webapp2.RequestHandler):
  def get(self):
    w1 = datetime.date(2014, 1, 7)
    w2 = datetime.date(2014, 1, 14)

    f = FakeData()
    f.createHighRuns()
    luckyShot = f.createLuckyShot()
    spr14 = f.createSeason()
    f.createPlayers(spr14)
    f.createWeek1(spr14, luckyShot, w1)
    f.createWeek2(spr14, luckyShot, w2)

    self.response.write('<html>\n')
    self.response.write('<head>\n')
    self.response.write('</head>\n')
    self.response.write('<body>\n')
    self.response.write('<p>Data has been generated. Click <a href="/">here</a> to go back to the main page.</p>\n')
    self.response.write('</body>\n')
    self.response.write('</html>\n')

class FakeData:
  def createHighRuns(self):
    # Create all the handicaps
    self.createHighRun(400, 18)
    self.createHighRun(450, 20)
    self.createHighRun(500, 22)
    self.createHighRun(550, 26)
    self.createHighRun(600, 32)
    self.createHighRun(650, 44)
    self.createHighRun(700, 58)
    self.createHighRun(725, 72)
    self.createHighRun(750, 86)
    self.createHighRun(775, 100)
    self.createHighRun(800, 114)
    self.createHighRun(825, 128)
    self.createHighRun(850, 144)

  def createHighRun(self, hcap, tgt):
    hrun = highRun.HighRun()
    hrun.handicap = hcap
    hrun.target = tgt
    hrun.put()

  # Create a Club
  def createLuckyShot(self):
    luckyShot = clubs.Club(key=ndb.Key(clubs.Club,'LS'))
    luckyShot.name = 'Lucky Shot'
    luckyShot.phone = '408-739-7665'
    luckyShot.put()
    return luckyShot
    
  # Create a Season
  def createSeason(self):
    spr14 = seasons.Season(key=ndb.Key(seasons.Season,'Spr14'))
    spr14.name = 'Spring 2014'
    spr14.startDate = datetime.date(2014, 1, 7)
    spr14.endDate = datetime.date(2014, 4, 30)
    spr14.put()
    return spr14
      
  # Create all the players
  def createPlayers(self, season):
    self.addPlayer(season, 'BenW', 'Ben', 'Wong', '', 718, 68.08)
    self.addPlayer(season, 'BobJ', 'Bob', 'Jewett', '', 763, 91.6)
    self.addPlayer(season, 'Brad', 'Brad', 'Jacobs', '', 609, 34.16)
    self.addPlayer(season, 'Chris', 'Chris', 'Koyama', '', 680, 49.6)
    self.addPlayer(season, 'CJ', 'CJ', 'Robinson', '', 717, 67.52)
    self.addPlayer(season, 'DPham', 'David', 'Pham', '', 549, 25.92)
    self.addPlayer(season, 'Eric', 'Eric', 'Harada', '', 770, 97.2)
    self.addPlayer(season, 'Henry', 'Henry', 'Lin', '', 586, 30.32)
    self.addPlayer(season, 'Horia', 'Horia', 'Udrea', '', 739, 79.84)
    self.addPlayer(season, 'Johonny', 'Johonny', 'Donoho', '', 695, 56.32)
    self.addPlayer(season, 'JoshR', 'Josh', 'Rousseau', '', 662, 47.36)
    self.addPlayer(season, 'Jud', 'Jud', 'Fitzmaurice', '', 674, 50.72)
    self.addPlayer(season, 'KimM', 'Kim', 'Merrill', '', 674, 50.72)
    self.addPlayer(season, 'Mark', 'Mark', 'Davidson', '', 727, 73.12)
    self.addPlayer(season, 'Noah', 'Noah', 'Zimmerman', '', 618, 36.32)
    self.addPlayer(season, 'Raj', 'Rajesh', 'Parvatheneni', '', 535, 24.8)
    self.addPlayer(season, 'Reid', 'Reid', 'Stensrud', '', 731, 75.36)
    self.addPlayer(season, 'Richard', 'Richard', 'Dweck', '', 577, 29.24)
    self.addPlayer(season, 'Shelby', 'Shelby', '***', '', 570, 28.4)
    self.addPlayer(season, 'Srivats', 'Srivats', 'Balachandran', '', 642, 42.08)
    self.addPlayer(season, 'SteveO', 'Steve', 'O\'Hara', '512-565-8626', 634, 40.16)
    self.addPlayer(season, 'Tony', 'Tony', 'Sugimoto', '', 485, 21.4)
    
  def addPlayer(self, season, key, first, last, phone, handicap, highrun):
    player = players.Player(key=ndb.Key(players.Player,key))
    player.firstName = first
    player.lastName = last
    player.phone = phone
    player.put()

    stat = stats.PlayerSummary()
    stat.player = player.key
    stat.season = season.key
    stat.handicap = handicap
    stat.highRunTarget = highrun
    stat.highRun = 0
    stat.wins = 0
    stat.losses = 0
    stat.put()

    return player

  # Jan 7, 2014 results
  def createWeek1(self, season, club, week):  
    self.addMatch(season, club, week, 'BenW', 718, 90, 35, 0, 'Reid', 731, 100, 100, 0)
    self.addMatch(season, club, week, 'SteveO', 634, 65, 55, 12, 'JoshR', 662, 80, 80, 15)
    self.addMatch(season, club, week, 'Richard', 577, 30, 30, 12, 'Mark', 727, 90, 49, 0)
    self.addMatch(season, club, week, 'Johonny', 695, 100, 49, 0, 'Tony', 485, 25, 25, 0)
    self.addMatch(season, club, week, 'Noah', 618, 50, 30, 0, 'Chris', 680, 80, 80, 13)
    self.addMatch(season, club, week, 'Horia', 739, 100, 100, 0, 'Johonny', 692, 70, 40, 0)
    self.addMatch(season, club, week, 'Tony', 488, 20, 16, 0, 'Mark', 724, 100, 100, 0)
    self.addMatch(season, club, week, 'Richard', 580, 50, 47, 0, 'Srivats', 642, 80, 80, 0)
    self.addMatch(season, club, week, 'BenW', 715, 100, 100, 20, 'SteveO', 634, 55, 50, 0)
    self.addMatch(season, club, week, 'KimM', 674, 90, 90, 0, 'JoshR', 665, 85, 55, 0)
    self.addMatch(season, club, week, 'DPham', 549, 55, 34, 0, 'Henry', 586, 70, 70, 0)
    self.addMatch(season, club, week, 'CJ', 717, 100, 100, 0, 'Chris', 690, 85, 40, 0)
    self.addMatch(season, club, week, 'Horia', 742, 100, 31, 0, 'Henry', 589, 35, 35, 0)
    self.addMatch(season, club, week, 'KimM', 677, 90, 77, 0, 'JoshR', 662, 85, 85, 0)

  # Jan 14, 2014 results
  def createWeek2(self, season, club, week):  
    self.addMatch(season, club, week, 'Reid', 731, 90, 59, 0, 'Eric', 770, 120, 120, 0)
    self.addMatch(season, club, week, 'Mark', 727, 90, 40, 0, 'Johonny', 694, 70, 70, 18)
    self.addMatch(season, club, week, 'JoshR', 662, 80, 0, 0, 'Brad', 609, 55, 55, 0)
    self.addMatch(season, club, week, 'Richard', 577, 45, 45, 0, 'Jud', 674, 90, 52, 0)
    self.addMatch(season, club, week, 'BobJ', 760, 120, 120, 0, 'BenW', 718, 90, 13, 0)
    self.addMatch(season, club, week, 'SteveO', 634, 55, 48, 0, 'Chris', 675, 80, 80, 14)
    self.addMatch(season, club, week, 'Shelby', 570, 70, 70, 0, 'Tony', 485, 40, 30, 0)
    self.addMatch(season, club, week, 'Mark', 724, 90, 90, 0, 'Jud', 671, 60, 58, 0)
    self.addMatch(season, club, week, 'BenW', 715, 100, 100, 0, 'Richard', 580, 40, 37, 0)
    self.addMatch(season, club, week, 'CJ', 720, 90, 90, 0, 'BobJ', 763, 120, 98, 0)
    self.addMatch(season, club, week, 'KimM', 674, 100, 48, 0, 'Henry', 586, 55, 55, 0)
    self.addMatch(season, club, week, 'JoshR', 662, 90, 90, 14, 'Shelby', 570, 50, 26, 0)
    self.addMatch(season, club, week, 'SteveO', 634, 90, 59, 0, 'Raj', 535, 45, 45, 10)
    self.addMatch(season, club, week, 'CJ', 720, 90, 65, 0, 'Henry', 589, 35, 35, 0)
    
  def addMatch(self, season, club, dat, p1, hc1, t1, s1, hr1, p2, hc2, t2, s2, hr2):
    match = matches.Match()
    match.date = dat
    match.season = season.key
    match.club = club.key
    player1 = players.Player.get_by_id(p1)
    player2 = players.Player.get_by_id(p2)
    
    if t1 == s1:
      logging.info('********************* W = %s, L = %s' % (player1.firstName, player2.firstName))
      match.playerW = player1.key
      match.handicapW = hc1
      match.scoreW = s1
      match.targetW = t1
      match.highRunW = hr1
      
      match.playerL = player2.key
      match.handicapL = hc2
      match.scoreL = s2
      match.targetL = t2
      match.highRunL = hr2
    elif t2 == s2:
      logging.info('********************* W = %s, L = %s' % (player2.firstName, player1.firstName))
      match.playerW = player2.key
      match.handicapW = hc2
      match.scoreW = s2
      match.targetW = t2
      match.highRunW = hr2
      
      match.playerL = player1.key
      match.handicapL = hc1
      match.scoreL = s1
      match.targetL = t1
      match.highRunL = hr1
    else:
      logging.error('********** Nobody won between %s and %s' % (p1.firstName, p2.firstName))
      pass

    # Save new match result
    match.put()
    
    # Update statistics for the winner and loser
    winner = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerW).fetch(1)[0]
    loser = stats.PlayerSummary.query(stats.PlayerSummary.player == match.playerL).fetch(1)[0]
    
    # Update win / loss totals
    winner.wins = winner.wins + 1
    loser.losses = loser.losses + 1

    # Update handicaps
    winner.handicap = winner.handicap + 3
    loser.handicap = loser.handicap - 3

    # Update high runs
    if match.highRunW > winner.highRun:
      winner.highRun = match.highRunW
    if match.highRunL > loser.highRun:
      loser.highRun = match.highRunL
    
    winner.put()
    loser.put()

app = webapp2.WSGIApplication([
   (r'/.*', FakeHandler)
], debug=True)
