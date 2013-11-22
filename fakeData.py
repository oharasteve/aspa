from google.appengine.ext import ndb
import datetime

import clubs
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
  
  def create(self):
    # Create a Club
    if clubs.Club.query().get() is None:
      luckyShot = clubs.Club(key=ndb.Key(clubs.Club,'LS'))
      luckyShot.name = 'Lucky Shot'
      luckyShot.phone = '408-739-7665'
      luckyShot.put()
    
    # Create a Season
    if seasons.Season.query().get() is None:
      fall13 = seasons.Season(key=ndb.Key(seasons.Season,'F13'))
      fall13.name = 'Fall 2013'
      fall13.startDate = datetime.date(2013, 7, 1)
      fall13.endDate = datetime.date(2013, 12, 1)
      fall13.put()
      
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
      
    # Create a player summary statistic
    if stats.PlayerSummary.query().get() is None:
      fall13 = seasons.Season.get_by_id('F13')
      
      steve13 = stats.PlayerSummary()
      steve13.player = players.Player.get_by_id('SteveO').key
      steve13.season = fall13.key
      steve13.handicap = 610
      steve13.highRunTarget = 41.84
      steve13.highRun = 14
      steve13.wins = 3
      steve13.losses = 10
      steve13.put()
      
      kim13 = stats.PlayerSummary()
      kim13.player = players.Player.get_by_id('KimM').key
      kim13.season = fall13.key
      kim13.handicap = 677
      kim13.highRunTarget = 45.4
      kim13.highRun = 18
      kim13.wins = 10
      kim13.losses = 6
      kim13.put()
      
      benw13 = stats.PlayerSummary()
      benw13.player = players.Player.get_by_id('BenW').key
      benw13.season = fall13.key
      benw13.handicap = 718
      benw13.highRunTarget = 68.08
      benw13.highRun = 62
      benw13.wins = 2
      benw13.losses = 2
      benw13.put()
