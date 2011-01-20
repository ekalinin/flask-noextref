from __future__ import with_statement

import urllib
import unittest
from flaskext.noextref import NoExtRef
from flask import Flask
from flask import redirect
from flask import abort
from flask import request
from flask import render_template_string


class NoExtRefTestCase(unittest.TestCase):

    def _create_noext(self, rule=None, view_func=None, safe_domains=[]):
        self.noext_url = '/test-ext-url-handler'

        app = Flask(__name__)
        app.config['TESTING'] = True
        app.test_request_context().push()
        client = app.test_client()

        if not rule:
            rule = '%s/<path:url>'%self.noext_url

        noext = NoExtRef(app, rule=rule, view_func=view_func,
                    safe_domains=safe_domains)
        return (client, noext)

    def test_hide_urls(self):
        client, noext = self._create_noext()
        text_tpl = 'some text with <a href="-=URL=-"> anchore </a>!!!!'
        text_ext_url = text_tpl.replace("-=URL=-",
            'http://www.appenginejob.com/job/152/Python-Developer/')
        text_loc_url = text_tpl.replace("-=URL=-",
            self.noext_url + '/' +
            'http://www.appenginejob.com/job/152/Python-Developer/')
        self.assertEqual(noext.hide_urls(text_ext_url), text_loc_url)

    def test_go_to_url(self):
        client, noext = self._create_noext()
        response = client.get(self.noext_url+'//')
        self.assertEqual(response.status_code, 404)

        test_url = 'http://www.appenginejob.com/about?test1=1&test2=2'
        response = client.get('%s/%s'%(self.noext_url, test_url))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], test_url)

    def test_hide_url_filter(self):
        client, noext = self._create_noext()
        test_url = 'http://www.appenginejob.com/about?test1=1&test2=2'
        tpl = "{% with -%}"+\
                    "{% set test_url = '"+test_url+"' %}" + \
                    "{{ test_url|hide_url }}" + \
              "{%- endwith %}"
        tpl_res = render_template_string(tpl)
        #tpl_res = urllib.unquote(tpl_res)
        self.assertEqual(tpl_res,u'%s/%s'%(self.noext_url, test_url))

    def test_hide_urls_filter(self):
        client, noext = self._create_noext()
        test_url = '<a href="http://www.odesk.com/jobs/Programming-Tutor_~~f7412e3478d07495?source=rss">View job &raquo;</a>'
        res_url  = '<a href="%s/http://www.odesk.com/jobs/Programming-Tutor_~~f7412e3478d07495?source=rss">View job &raquo;</a>'%(\
                    self.noext_url)
        tpl = "{% set test_url = '"+test_url+"' %}" + \
                    "{{ test_url|hide_urls }}" 
        tpl_res = render_template_string(tpl)
        #tpl_res = urllib.unquote(tpl_res)
        self.assertEqual(tpl_res,res_url)

    def test_hide_urls_safe_domain(self):
        client, noext = self._create_noext(safe_domains=['appenginejob.com'])

        text_tpl = 'some text with <a href="-=URL=-"> anchore </a>!!!!'
        text_url = text_tpl.replace("-=URL=-",
            'http://www.appenginejob.com/job/152/Python-Developer/')
        self.assertEqual(noext.hide_urls(text_url), text_url)

    def test_url_handler(self):
        def custom_view_func():
            url = request.args.get('url', None)
            if not url:
                abort(405)
            args = '&'.join( '%s=%s'%(key, value) for key, value \
                        in request.args.iteritems() if key != 'url')
            return redirect('%s&%s'%(url, args))

        test_url = 'http://www.appenginejob.com/about/?test=1&test=2'
        ext_url = '/ext-test-url/'
        c, noext = self._create_noext(rule=ext_url,
                view_func=custom_view_func)

        response = c.get(noext.hide_url(test_url))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], test_url)

        response = c.get(ext_url)
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
