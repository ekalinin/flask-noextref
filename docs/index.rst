==============
Flask-NoExtRef
==============

.. module:: flaskext.noextref

Flask-NoExtRef is an extension for `Flask`_ that adds ability for 
hiding external URL to your Flask application.

.. _Flask: http://flask.pocoo.org/

Installation
------------

Install the extension with one of the following commands::

    $ easy_install Flask-NoExtRef

or alternatively if you have pip installed::

    $ pip install Flask-NoExtRef

How to Use
----------

Basically all you have to do is to create an :class:`NoExtRef` object.
After that you can use objects's methods in your python code or can use 
new filters in `Jinja`_ templates with the same names for hiding external 
URL. Here is a complete example:

>>> from flask import Flask
>>> from flaskext.noextref import NoExtRef
>>> app = Flask(__name__)
>>> noext = NoExtRef(app)
>>> # these line of code is necessary in console only
>>> app.test_request_context().push()
>>> print noext.hide_url("http://google.com")
/ext-url/http://google.com
>>> print noext.hide_urls('test <a href="http://google.com"> anchor </a> ')
test <a href="/ext-url/http://google.com"> anchor </a>

And this is an example of using new filters in Jinja templates:

.. code-block:: jinja

    {# replace all anchors in the text #}
    {{ some_text_with_refs|hide_urls }}

    {# replace of the specified anchor #}
    {{ some_url|hide_url }}

In the default configuration all external path will be hidden as::

    /ext-url/<path:url>

.. _Jinja: http://jinja.pocoo.org/

How to change
-------------

If the default settings are not suitable for you then you can easily 
change them. For example if you want to set different format for hide 
external URL::

    /go?url=external-url

You must do the following::

    from flask import Flask, abort, request, redirect
    from flaskext.noextref import NoExtRef

    app = Flask(__name__)

    def handle_ext_url():
        url = request.args.get('url', None)
        if not url:
            abort(405)
        return redirect(url)

    noext = NoExtRef(app, rule='/go/',
                view_func=handle_ext_url)


If you do not want to hide urls from some domain do the follow::

    from flask import Flask, abort, request, redirect
    from flaskext.noextref import NoExtRef

    app = Flask(__name__)
    noext = NoExtRef(app, safe_domains=['some-domain.com'])


Api
---

This part of the documentation documents all the public classes and
functions in Flask-NoExtRef.

.. autoclass:: NoExtRef
    :members:


Robots.txt
----------

Default `robots.txt`_::

    User-agent: *
    Disallow: /ext-url/ 

.. _robots.txt: http://en.wikipedia.org/wiki/Robots_exclusion_standard 

.. include:: ../CHANGES
