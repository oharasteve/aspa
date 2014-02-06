from google.appengine.ext import ndb
import logging

class HighRun(ndb.Model):
    """Models high run targets for a handicap."""
    handicap = ndb.IntegerProperty()
    target = ndb.IntegerProperty()

    @classmethod
    def getHighRuns(self):
        return [ item.to_dict() for item in self.query().order(HighRun.handicap) ]
