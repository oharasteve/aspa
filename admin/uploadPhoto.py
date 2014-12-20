#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers

import base_handler
import datetime
import webapp2

from data import players

TEMPLATE = 'html/add_photo.html'

class PostPhotoHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        xplayer = self.request.get('player_select')
        upload_files = self.get_uploads('upload')  # 'file' is file upload field in the form
        blob_info = upload_files[0]

        error_messages = []
        player = players.Player.get_by_id(xplayer)
        if not player:
            error_messages.append("Player is required")

        display_form = False

        if not len(error_messages):
            # Update photo for the player
            playerList = players.Player.query(
                players.Player.key == player.key).fetch(1)
            if playerList:
              player = playerList[0]
              player.photo = images.get_serving_url(blob_info)
              player.put()
              display_form = True
            else:
              error_messages.append("Unable to find %s" % player)

        self.redirect('/admin/addPhoto/')

app = webapp2.WSGIApplication([(r'/.*', PostPhotoHandler)],
    debug=True,
    config=base_handler.CONFIG)
