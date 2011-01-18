# -*- coding: utf-8 -*-
"""
    flaskext.noextref
    ~~~~~~~~~~~~~~~~~

    Provides support for hiding external URLs for
    sites based on Flask.

    :copyright: (c) 2011 by Eugene Kalinin.
    :license: BSD, see LICENSE for more details.
"""

import re
import urlparse

from flask import abort
from flask import url_for
from flask import redirect
from flask import request


# TODO:
#   * docstring, описание переменных, методов
#   * документация - добавить logo
#   * защита от двойной инициализации
#       * выставлять app.noext
#       * проверять при инициализации класса app.noext.
#         Если он есть, то возвращять его. 
#       * Тест!!!

class NoExtRef(object):
    """ """

    NOEXTREF_RE = re.compile('href="(?P<url>.*)"', re.IGNORECASE|re.UNICODE)

    def __init__(self, app, rule='/ext-url/<path:url>', endpoint='ext_url', 
                    view_func=None, safe_domains=[]):
        self.app = app
        self.rule = rule
        self.endpoint = endpoint
        if isinstance(safe_domains, list):
            self.safe_domains = safe_domains
        elif safe_domains:
            self.safe_domains = [safe_domains]

        if view_func is None:
            view_func = self.go_to_url
        self.app.add_url_rule(self.rule, self.endpoint, view_func)

        self.app.jinja_env.filters.update(
            hide_url=self.hide_url,
            hide_urls=self.hide_urls
        )

    def go_to_url(self, url):
        """Redirects to the external 'url'"""
        args = '&'.join( '%s=%s'%(key, value) for key, value \
                    in request.args.iteritems() )
        return redirect('%s?%s'%(url, args))

    def hide_url(self, url):
        """
        Converts external 'url' to the local URL.
        Also available in Jinja templates as 'hide_url' filter.
        """
        for u in self.safe_domains:
            if u in url:
                return url
        return url_for(self.endpoint, url=url)

    def hide_urls(self, text):
        """Find all references (href) in the 'text' 
        and replaces them with local"""
        def href_repl(m):
            if m:
                url = m.group(1)
                return 'href="%s"' % self.hide_url(url)
            return m

        return self.NOEXTREF_RE.sub(href_repl, text)


# ---------------------------------------------------------
# robots.txt for hide redirect path
# ---------------------------------------------------------
