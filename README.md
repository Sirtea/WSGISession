# WSGISession

WSGISession provides an easy way to deal with sessions in any WSGI
compilant application. This middleware is useful always you want to
store user sessions of a user, understanding that this user will store
the session id in a cookie. It's up to you how to save and retrieve
the session object.

WSGISession has a pair of objects to use: SessionMiddleware and Session.

## How to use SessionMiddleware

SessionMiddleware is a middleware, wrapping your application.
An instance of the SessionMiddleware object is a WSGI application
that behaves like a WSGI callable. Once the WSGI server calls a
SessionMiddleware instance, the callable method passes the call to the
wrapped WSGI callable, appending a Session object that corresponds to the
session id stored on a cookie. When calling the start_response method,
it also saves the session object and stores the session id in the
cookie. The work of load and retrieve the session based on the id is
provided by a factory that must be written by yourself. Learn by example:

```python
#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgisession import SessionMiddleware


class ExampleFactory(object):
    def load(self, id):
        session = Session()
        # whatever needed to retireve session object
        session.data = {'dummy': 'key'}
        session.id = '123'
        return session

    def save(self, session):
        # save the session.data, possibly generating session.id
        return session.id


def wrapped_app(environ, start_response):
    session = environ.get('wsgisession')
    session['counter'] = session.get('counter', 0) + 1
    start_response('200 OK', [('Content-Type', 'text/html')])
    return 'Visited %s times\n' % session['counter']

factory = ExampleFactory()
app = SessionMiddleware(wrapped_app, factory)

if __name__ == '__main__':
    httpd = make_server('localhost', 8080, app)
    httpd.serve_forever()
```

## How to use Session

Session is a convenience object, that stores data and the session id.
When created, session.data and session.id are initialized to {} and None.
It's your factory the responsible to fill those fields.

This object have also convenient methods for easy access to the data,
using the form Session[key], and also a method Session.get() with a
default option.

## How to implement a SessionFactory

The SessionFactory object is the responsible to load and store the
Session data wherever it goes (it's up to you!!!). This object must
implement only two methods (more if you need):

* load(id): loads the id and returns a Session object.
* save(session): saves the session and returns the id to load later

The session id goes "as is" to the cookie, so it's up to you to
protect them if they are sensible enough.
