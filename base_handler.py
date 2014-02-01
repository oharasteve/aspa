"""Base handler class."""
#!/usr/bin/env python

# From http://webapp-improved.appspot.com/api/webapp2_extras/jinja2.html
import os
import webapp2

from webapp2_extras import jinja2


def datetimeformat(value, format='%b %d, %Y'):
    return value.strftime(format)


CONFIG = {
    'webapp2_extras.jinja2': {
        'template_path': os.path.dirname(__file__),
        'filters': {
            'datetimeformat': datetimeformat,
            },
        }
    }


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rendered_output = self.jinja2.render_template(_template, **context)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(rendered_output)
