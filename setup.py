from distutils.core import setup

setup(
    name='WSGISession',
    version='0.1.1',
    author='Gerard Monells',
    author_email='gerard.monells@gmail.com',
    url='https://github.com/Sirtea/WSGISession',
    py_modules=['wsgisession'],
    license='MIT license',
    description='WSGI sessions implentation (session id in a cookie).',
    long_description=open('README.txt').read(),
    platforms='any',
    download_url='http://pypi.python.org/pypi/WSGISession/',
)
