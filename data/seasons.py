from google.appengine.ext import ndb
from data import clubs

#
# One row per season. Typically 2-3 seasons per year
#


class Season(ndb.Model):
    """Models a playing season."""
    name = ndb.StringProperty()
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    weeks = ndb.IntegerProperty(default=0)
    club = ndb.KeyProperty(kind=clubs.Club)

    @classmethod
    def getSeasons(self, club):
        ret_list = []

        for item in self.query(self.club == club.key).order(-Season.startDate):
            my_dict = item.to_dict()
            my_dict['id'] = item.key.id()
            ret_list.append(my_dict)
        return ret_list

