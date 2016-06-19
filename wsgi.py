import tornado.wsgi
from config import Application

application = tornado.wsgi.WSGIAdapter(Application)