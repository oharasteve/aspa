# From https://developers.google.com/appengine/docs/python/blobstore/
# Aug 2, 2014

import logging
import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    if blob_info:
      logging.info('******** Serving %s (%d bytes)', blob_info.filename, blob_info.size)
      self.send_blob(blob_info)

app = webapp2.WSGIApplication([('/showResults/([^/]+)?', ServeHandler)],
                              debug=True)
