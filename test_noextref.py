from __future__ import with_statement

import urllib
import unittest
from flaskext.noextref import NoExtRef
import flask
from flask import redirect


class NoExtRefTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        self.noext_url = '/test-ext-url-handler'
        self.noext = NoExtRef(app=self.app, rule='%s/<path:url>'%self.noext_url)

    def test_hide_urls(self):
        text_tpl = 'some text with <a href="-=URL=-"> anchore </a>!!!!'
        text_ext_url = text_tpl.replace("-=URL=-",
            'http://www.appenginejob.com/job/152/Python-Developer/')
        text_loc_url = text_tpl.replace("-=URL=-",
            self.noext_url + '/' +
            'http://www.appenginejob.com/job/152/Python-Developer/')
        self.assertEqual(self.noext.hide_urls(text_ext_url), text_loc_url)

    def test_go_to_url(self):
        response = self.client.get(self.noext_url+'//')
        self.assertEqual(response.status_code, 404)

        test_url = 'http://www.appenginejob.com/about?test1=1&test2=2'
        response = self.client.get('%s/%s'%(self.noext_url, test_url))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], test_url)

    def test_hide_urls_filter(self):
        test_url = 'http://www.appenginejob.com/about?test1=1&test2=2'
        tpl = "{% with -%}"+\
                    "{% set test_url = '"+test_url+"' %}" + \
                    "{{ test_url|hide_url }}" + \
              "{%- endwith %}"
        tpl_res = flask.render_template_string(tpl)
        tpl_res = urllib.unquote(tpl_res)
        self.assertEqual(tpl_res,u'%s/%s'%(self.noext_url, test_url))

    def test_hide_urls_safe_domain(self):
        a = flask.Flask(__name__)
        a.config['TESTING'] = True
        a.debug = True
        c = a.test_client()

        noext = NoExtRef(app=a, safe_domains=['appenginejob.com'])

        text_tpl = 'some text with <a href="-=URL=-"> anchore </a>!!!!'
        text_url = text_tpl.replace("-=URL=-",
            'http://www.appenginejob.com/job/152/Python-Developer/')
        self.assertEqual(noext.hide_urls(text_url), text_url)

    def test_url_handler(self):
        a = flask.Flask(__name__)
        a.config['TESTING'] = True
        a.debug = True
        c = a.test_client()

        def custom_view_func(url):
            return redirect('http://www.google.com')

        noext = NoExtRef(app=a, view_func=custom_view_func)
        response = c.get('/ext-url/http://www.appenginejob.com/about/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], 'http://www.google.com')

if __name__ == '__main__':
    unittest.main()
