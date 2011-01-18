Flask-NoExtRef
==============

.. module:: flaskext.noextref

Flask-NoExtRef is an extension for `Flask`_ that adds hiding 
external URLs support to your Flask application.

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
After that you can use it's methods in your python code or user appropriate
filters in `Jinja`_ templates for hiding external URLs.
Here is a complete example::

    >>> from flask import Flask
    >>> from flaskext.noextref import NoExtRef

    >>> app = Flask(__name__)
    >>> noext = NoExtRef(app)

    >>> # these two lines of code are necessary in console only
    >>> ctx = app.test_request_context()
    >>> ctx.push()

    >>> print noext.hide_url("http://google.com")
    /ext-url/http://google.com
    >>> print noext.hide_urls('test <a href="http://google.com"> anchore </a> ')
    test <a href="/ext-url/http://google.com"> anchore </a> 

Or you can use appropriate filters in Jinja templates::

    {{ some_text_with_refs|hide_urls }}
