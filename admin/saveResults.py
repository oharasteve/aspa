# From https://developers.google.com/appengine/docs/python/blobstore/
# Aug 2, 2014

import logging
import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class SaveHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/admin/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    logging.info('******** Uploading %s', blob_info.key())
    self.redirect('/showResults/%s' % blob_info.key())

app = webapp2.WSGIApplication([('/admin/saveResults/', SaveHandler),
                               ('/admin/upload', UploadHandler),
                              ],
                              debug=True)
