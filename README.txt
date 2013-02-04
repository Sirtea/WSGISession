===========
WSGISession
===========

WSGISession provides an easy way to deal with sessions in any WSGI
compilant application. This middleware is useful always you want to
store user sessions of a user, understanding that this user will store
the session id in a cookie. It's up to you how to save and retrieve
the session object.

In order to do so, we offer the middleware and the session object, but
you need to provide the session factory object, whose role is to save
and retrieve sessions from wherever they are. Here's an example:

    #!/usr/bin/env python

    from wsgiref.simple_server import make_server
    from wsgisession import SessionMiddleware


    class ExampleFactory(object):
        def load(self, id=None):
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
