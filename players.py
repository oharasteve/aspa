from google.appengine.ext import ndb

class Player(ndb.Model):
    """Models a player."""
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    phone = ndb.StringProperty()

    @classmethod
    def getPlayers(self):
        ret_list = []
        for item in self.query().order(Player.firstName, Player.lastName):
            my_dict = item.to_dict()
            my_dict['id'] = item.key.id()
            ret_list.append(my_dict)
        return ret_list
