from google.appengine.ext import ndb

#
# One row per player, regardless of how many seasons they play
#

class Player(ndb.Model):
    """Models a player."""
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    photo = ndb.StringProperty()
    handicap = ndb.IntegerProperty()
    seasons = ndb.KeyProperty(repeated=True)

    @classmethod
    def getPlayers(self):
        ret_list = []
        for item in self.query().order(Player.firstName, Player.lastName):
            my_dict = item.to_dict()
            my_dict['id'] = item.key.id()
            ret_list.append(my_dict)
        return ret_list
