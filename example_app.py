#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgisession import SessionMiddleware
from example_factory import MongoSessionFactory


def wrapped_app(environ, start_response):
    session = environ.get('wsgisession')
    session['counter'] = session.get('counter', 0) + 1
    start_response('200 OK', [('Content-Type', 'text/html')])
    return 'Visited %s times\n' % session['counter']

factory = MongoSessionFactory('sessiondb', ttl=300)
app = SessionMiddleware(wrapped_app, factory)

if __name__ == '__main__':
    httpd = make_server('localhost', 8080, app)
    httpd.serve_forever()
