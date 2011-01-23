# -*- coding: utf-8 -*-
"""
    flaskext.noextref
    ~~~~~~~~~~~~~~~~~

    Provides support for hiding external URL for
    sites based on Flask.

    :copyright: (c) 2011 by Eugene Kalinin.
    :license: BSD, see LICENSE for more details.
"""

import re
import urllib

from flask import abort
from flask import url_for
from flask import redirect
from flask import request


class NoExtRef(object):
    """NoExtRef object adds ability to the Flask application to hide
    external URL. Change the state of the Flask application: adds Jinja
    filters and creates back reference (app._noextref).

    :param app: the :class:`Flask` application
    :param rule: the URL rule as string
    :param endpoint: the endpoint for the registered URL rule
    :param view_func: the function to call when serving a request
                      to the provided endpoint
    :param safe_domains: the list of domains that are not external.
                         URL containing one of these domains will
                         not be hidden.
    :param add_jinja_filters: if True then adds new filters for Jinja
    """

    NOEXTREF_RE = re.compile('href="(?P<url>.*)"', re.IGNORECASE|re.UNICODE)

    def __init__(self, app, rule='/ext-url/<path:url>', endpoint='ext_url', 
                    view_func=None, safe_domains=[], add_jinja_filters=True):
        self.app = app
        self.rule = rule
        self.endpoint = endpoint
        if isinstance(safe_domains, list):
            self.safe_domains = safe_domains
        elif safe_domains:
            self.safe_domains = [safe_domains]

        if hasattr(self.app, '_noextref'):
            return

        if view_func is None:
            view_func = self.go_to_url
        self.app.add_url_rule(self.rule, self.endpoint, view_func)

        if add_jinja_filters:
            self.app.jinja_env.filters.update(
                hide_url=self.hide_url,
                hide_urls=self.hide_urls
            )

        self.app._noextref = self

    def go_to_url(self, url):
        """Redirects to the external `url`"""
        args = '&'.join( '%s=%s'%(key, value) for key, value \
                    in request.args.iteritems() )
        return redirect('%s?%s'%(url, args))

    def hide_url(self, url):
        """
        Converts external `url` to the local URL.
        Also available in Jinja templates as filter.
        """
        for u in self.safe_domains:
            if u in url:
                return url
        return urllib.unquote(url_for(self.endpoint, url=url))

    def hide_urls(self, text):
        """
        Finds all references (href) in the `text` and replaces
        them with local. Also available in Jinja templates as filter.
        """
        def href_repl(m):
            if m:
                url = m.group(1)
                return 'href="%s"' % self.hide_url(url)
            return m

        return self.NOEXTREF_RE.sub(href_repl, text)
