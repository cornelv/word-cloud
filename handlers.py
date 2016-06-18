import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return False
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")