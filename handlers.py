import tornado.web
from tornado.escape import json_encode

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")


class ScrapeHandler(BaseHandler):
    def post(self):

    	url = self.get_argument("url")


        self.write(json_encode({"result": url}))
