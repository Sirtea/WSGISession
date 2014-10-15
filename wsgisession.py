from Cookie import SimpleCookie


class Session(object):

    def __init__(self):
        self.id = None
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        try:
            del self.data[key]
        except KeyError:
            pass

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default


class SessionMiddleware(object):

    def __init__(self, app, factory,
                 env_key='wsgisession', cookie_key='session_id'):
        self.app = app
        self.factory = factory
        self.env_key = env_key
        self.cookie_key = cookie_key

    def __call__(self, environ, start_response):
        cookie = SimpleCookie()
        if 'HTTP_COOKIE' in environ:
            cookie.load(environ['HTTP_COOKIE'])
        id = None
        if self.cookie_key in cookie:
            id = cookie[self.cookie_key].value
        environ[self.env_key] = self.factory.load(id)

        def middleware_start_response(status, response_headers, exc_info=None):
            id = self.factory.save(environ[self.env_key])
            cookie = SimpleCookie()
            cookie[self.cookie_key] = id
            cookie[self.cookie_key]['path'] = '/'
            cookie_string = cookie[self.cookie_key].OutputString()
            response_headers.append(('Set-Cookie', cookie_string))
            return start_response(status, response_headers, exc_info)
        return self.app(environ, middleware_start_response)
