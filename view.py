"""Class to present the View."""
import cgi
import logging
import players
import stats

VIEW_TEMPLATE = "html/view.html"

class View():

    def get_player_summaries(self, season):
        entries = []
        if not season:
            return entries
        seq = 0
        summaries = stats.PlayerSummary.query( stats.PlayerSummary.season ==
                season.key).order( -stats.PlayerSummary.wins).order(
                        stats.PlayerSummary.losses)
        for summary in summaries:
            player = players.Player.get_by_id(summary.player.id())
            seq += 1

            player_summary = {
                'entry_index': seq,
                'summary': summary,
                'player': players.Player.get_by_id(summary.player.id()),
                'details_page_url':
                'details/?Season={0}&Player={1}'.format(
                    cgi.escape(season.key.id()),
                    cgi.escape(summary.player.id())),
                'season': season,
                'alternate_class': 'even' if seq % 2 == 0 else 'odd',
                }
            entries.append(player_summary)
        logging.debug('Found %d player summary records' % (len(entries)))
        return entries

    def get_template_values(self, season):
        player_summaries = self.get_player_summaries(season)
        template_values = {
                'season': season,
                'player_summaries': player_summaries,
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
        return template_values

    def showPage(self, jinja_environment, response, season):
        template = jinja_environment.get_template(VIEW_TEMPLATE)
        template_values = self.get_template_values(season)
        response.write(template.render(template_values))
