import cgi
import datetime

import players
import stats

class View():
  def getEntries(self, season):
    entries = []
    if not season:
      return entries

    seq = 0
    summaries = stats.PlayerSummary.query(stats.PlayerSummary.season == season.key).order(-stats.PlayerSummary.wins).order(stats.PlayerSummary.losses)
    for summary in summaries:
      player = players.Player.get_by_id(summary.player.id())
      seq += 1

      template_values = {
        'entry_index': seq,
        'summary': summary,
        'player': players.Player.get_by_id(summary.player.id()),
        'details_page_url': 'details/?Season={0}&Player={1}'.format(cgi.escape(season.key.id()), cgi.escape(summary.player.id())),
        'season': season,
        'alternate_class': 'even' if seq % 2 == 0 else 'odd',
      }
      entries.append(template_values)
    return entries

  def showPage(self, jinja_environment, response, season):
    template = jinja_environment.get_template('html/view.html')
    entries = self.getEntries(season)
    template_values = {
        'season': season,
        'entries': entries,
        'site_admin': {
          'email': 'site_admin_email',
          'name': 'site_admin_name',
          },
        'league_manager': {
          'email': 'league_manager_email',
          'name': 'league_manager_name',
          },
        'page': {
          'last_updated_date': '2014-01-27 12:00:00',
          },
    }
    response.write(template.render(template_values))

