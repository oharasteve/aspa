# From https://developers.google.com/appengine/docs/python/blobstore/
# Aug 2, 2014

import logging
import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.api import users

from google.appengine.ext.webapp import blobstore_handlers

from data import clubs

class SaveHandler(webapp2.RequestHandler):
  def get(self, clubid):
    club = clubs.Club.get_by_id(clubid)
    if club == None:
       clubs.sendNoSuch(clubid)
       return
    user = users.get_current_user()
    if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
        self.response.clear()
        self.response.set_status(405)
        self.response.out.write("Not authorized")
        return
    if user not in club.owners:
         club.owners.append(user)
         club = club.put()
    upload_url = blobstore.create_upload_url('/%s/admin/upload'%(club.key.id(),))
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self, clubid):
    club = clubs.Club.get_by_id(clubid)
    if club == None:
       clubs.sendNoSuch(clubid)
       return
    user = users.get_current_user()
    if user not in club.owners and user.email() not in club.invited and not users.is_current_user_admin():
        self.response.clear()
        self.response.set_status(405)
        self.response.out.write("Not authorized")
        return
    if user not in club.owners:
        club.owners.append(user)
        club = club.put()
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    logging.info('******** Uploading %s', blob_info.key())
    self.redirect('/showResults/%s' % (blob_info.key(),))

app = webapp2.WSGIApplication([('/([^/]*)/admin/saveResults/', SaveHandler),
                               ('/([^/]*)/admin/upload', UploadHandler),
                              ],
                              debug=True)
