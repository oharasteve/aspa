from google.appengine.ext import ndb

#
# One row per season. Typically 2-3 seasons per year
#

class Season(ndb.Model):
    """Models a playing season."""
    name = ndb.StringProperty()
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    weeks = ndb.IntegerProperty(default=0)

    @classmethod
    def getSeasons(self):
        ret_list = []
        for item in self.query().order(-Season.startDate):
            my_dict = item.to_dict()
            my_dict['id'] = item.key.id()
            ret_list.append(my_dict)
        return ret_list

