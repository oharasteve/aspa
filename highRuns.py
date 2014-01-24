import stats

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    season_name = self.request.get('season')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(100)

    for greeting in greetings:
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                    cgi.escape(guestbook_name)))