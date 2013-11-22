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
import webapp2

import addMatch
import addPerson
import fakeData
import highRun
import seasons
import suggestMatch
import view

class MainHandler(webapp2.RequestHandler):
  def get(self):
    # Destroy or create fake data
    #f = fakeData.FakeData()
    #f.destroy()
    #f.create()
    
    hr = highRun.HighRun()
    #hr.destroy()
    hr.create()

    season = seasons.Season.get_by_id('F13')

    # Show the webpage
    v = view.View()
    v.header(self.response, season)
    v.show(self.response, season)
    
    ap = addPerson.AddPerson()
    ap.show(self.response)
    
    am = addMatch.AddMatch()
    am.show(self.response, season)
    
    sm = suggestMatch.SuggestMatch()
    sm.show(self.response, season)
    
    v.footer(self.response)
      
app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
