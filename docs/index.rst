Flask-NoExtRef
==============

.. module:: flaskext.noextref

Flask-NoExtRef is an extension to 'Flask'_ that adds hiding 
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

Basically all you have to do is to create an :class:`NoExtRef` object
and use this.  Here is a complete example::

    from flask import Flask
    from flaskext.noextref import NoExtRef

    app = Flask(__name__)
    noext = NoExtRef(app)

That is all! After this moment you can use filters:

  * :meth:`~NoExtRef.hide_url`
  * :meth:`~NoExtRef.hide_urls`
