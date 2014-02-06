from google.appengine.ext import ndb

class Club(ndb.Model):
    """Models the club locations."""
    name = ndb.StringProperty()
    phone = ndb.StringProperty()

    @classmethod
    def getClubs(self):
        return [ item.to_dict() for item in self.query().order(Club.name) ]
