from google.appengine.ext import ndb
import datetime

import clubs
import matches
import players
import seasons
import stats
import view

class FakeData():
  def destroy(self):
    # Delete all old data
    ndb.delete_multi(stats.PlayerSummary.query().fetch(keys_only=True))
    ndb.delete_multi(players.Player.query().fetch(keys_only=True))
    ndb.delete_multi(seasons.Season.query().fetch(keys_only=True))
    ndb.delete_multi(clubs.Club.query().fetch(keys_only=True))
    ndb.delete_multi(matches.Match.query().fetch(keys_only=True))
  
  def create(self):
    # Create a Club
    if clubs.Club.query().get() is None:
      luckyShot = clubs.Club(key=ndb.Key(clubs.Club,'LS'))
      luckyShot.name = 'Lucky Shot'
      luckyShot.phone = '408-739-7665'
      luckyShot.put()
    
    # Create a Season
    if seasons.Season.query().get() is None:
      spr14 = seasons.Season(key=ndb.Key(seasons.Season,'Spr14'))
      spr14.name = 'Spring 2014'
      spr14.startDate = datetime.date(2014, 1, 7)
      spr14.endDate = datetime.date(2014, 4, 30)
      spr14.put()
      
    # Create a player
    if players.Player.query().get() is None:
      steveo = players.Player(key=ndb.Key(players.Player, 'SteveO'))
      steveo.firstName = 'Steve'
      steveo.lastName = 'O\'Hara'
      steveo.phone = '512-565-8626'
      steveo.put()
      
      kimm = players.Player(key=ndb.Key(players.Player, 'KimM'))
      kimm.firstName = 'Kim'
      kimm.lastName = 'Merrill'
      kimm.phone = ''
      kimm.put()

      benw = players.Player(key=ndb.Key(players.Player, 'BenW'))
      benw.firstName = 'Ben'
      benw.lastName = 'Wong'
      benw.phone = ''
      benw.put()
      
      reid = players.Player(key=ndb.Key(players.Player, 'Reid'))
      reid.firstName = 'Reid'
      reid.lastName = 'Stensrud'
      reid.phone = ''
      reid.put()
      
      joshr = players.Player(key=ndb.Key(players.Player, 'JoshR'))
      joshr.firstName = 'Josh'
      joshr.lastName = 'Rousseau'
      joshr.phone = ''
      joshr.put()
      
    # Create a player summary statistic
    if stats.PlayerSummary.query().get() is None:
      spr14 = seasons.Season.get_by_id('Spr14')
      
      steve = stats.PlayerSummary()
      steve.player = players.Player.get_by_id('SteveO').key
      steve.season = spr14.key
      steve.handicap = 622
      steve.highRunTarget = 40.16
      steve.highRun = 12
      steve.wins = 0
      steve.losses = 4
      steve.put()
      
      kim = stats.PlayerSummary()
      kim.player = players.Player.get_by_id('KimM').key
      kim.season = spr14.key
      kim.handicap = 671
      kim.highRunTarget = 50.72
      kim.highRun = 0
      kim.wins = 1
      kim.losses = 2
      kim.put()
      
      benw = stats.PlayerSummary()
      benw.player = players.Player.get_by_id('BenW').key
      benw.season = spr14.key
      benw.handicap = 718
      benw.highRunTarget = 68.08
      benw.highRun = 20
      benw.wins = 2
      benw.losses = 2
      benw.put()
      
      reid = stats.PlayerSummary()
      reid.player = players.Player.get_by_id('Reid').key
      reid.season = spr14.key
      reid.handicap = 731
      reid.highRunTarget = 75.36
      reid.highRun = 0
      reid.wins = 1
      reid.losses = 1
      reid.put()
      
      joshr = stats.PlayerSummary()
      joshr.player = players.Player.get_by_id('JoshR').key
      joshr.season = spr14.key
      joshr.handicap = 665
      joshr.highRunTarget = 47.36
      joshr.highRun = 15
      joshr.wins = 3
      joshr.losses = 2
      joshr.put()
      
    # Create some match results
    if matches.Match.query().get() is None:
      spr14 = seasons.Season.get_by_id('Spr14')
      
      match1 = matches.Match()
      match1.date = datetime.date(2014, 1, 7)
      match1.season = spr14.key
      match1.club = clubs.Club(key=ndb.Key(clubs.Club,'LS')).key
      
      match1.playerW = players.Player.get_by_id('Reid').key
      match1.handicapW = 731
      match1.scoreW = 100
      match1.targetW = 100
      match1.highRunW = 0
      
      match1.playerL = players.Player.get_by_id('BenW').key
      match1.handicapL = 718
      match1.scoreL = 35
      match1.targetL = 90
      match1.highRunL = 0
      match1.put()

      match2 = matches.Match()
      match2.date = datetime.date(2014, 1, 7)
      match2.season = spr14.key
      match2.club = clubs.Club(key=ndb.Key(clubs.Club,'LS')).key
      
      match2.playerW = players.Player.get_by_id('JoshR').key
      match2.handicapW = 662
      match2.scoreW = 80
      match2.targetW = 80
      match2.highRunW = 15
      
      match2.playerL = players.Player.get_by_id('SteveO').key
      match2.handicapL = 634
      match2.scoreL = 55
      match2.targetL = 65
      match2.highRunL = 12
      match2.put()
