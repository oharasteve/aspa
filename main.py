#!/usr/bin/env python
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

import logging
import os
import urllib

import jinja2
import seasons
import shared
import view
import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        season = seasons.Season.get_by_id('Spr14')

        # Show the webpage
        v = view.View()
        v.showPage(JINJA_ENVIRONMENT, self.response, season)


def datetimeformat(value, format='%b %d, %Y'):
    return value.strftime(format)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['datetimeformat'] = datetimeformat

app = webapp2.WSGIApplication([ (r'/', MainHandler) ], debug=True)
