from google.appengine.ext import ndb

#
# One row per Club. No dependencies. Based on a physical location.
#

class Club(ndb.Model):
    """Models the club locations."""
    name = ndb.StringProperty()
    address1 = ndb.StringProperty(default='')
    address2 = ndb.StringProperty(default='')
    contact = ndb.StringProperty(default='')
    phone = ndb.StringProperty()
    owners = ndb.UserProperty(repeated=True)
    invited = ndb.StringProperty(repeated=True)

    @classmethod
    def getClubs(self):
        ret_list = []
        for item in self.query().order(Club.name):
            my_dict = item.to_dict()
            my_dict['id'] = item.key.id()
            ret_list.append(my_dict)
        return ret_list
