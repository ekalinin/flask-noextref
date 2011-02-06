"""
Flask-NoExtRef
--------------

Provides support for hiding external URL for
sites based on Flask.

Links
`````

* `documentation <http://packages.python.org/Flask-NoExtRef>`_
* `development version
  <http://github.com/ekalinin/flask-noextref/zipball/master#egg=Flask-NoExtRef-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-NoExtRef',
    version='0.1',
    url='http://github.com/ekalinin/flask-noextref',
    license='BSD',
    author='Eugene Kalinin',
    author_email='e.v.kalinin@gmail.com',
    description='Support for hiding external URL',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    test_suite='test_noextref.NoExtRefTestCase',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
