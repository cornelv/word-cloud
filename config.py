import os
import tornado.web
import torndb
from tornado.options import define, options

from handlers import HomeHandler, ScrapeHandler


define("port", default=8000, help="run on the given port", type=int)

define("mysql_host", default="127.0.0.1:3306")
define("mysql_database", default="wordcount")
define("mysql_user", default="wordcount")
define("mysql_password", default="12345678")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/scrape/", ScrapeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="87t7868&T^&RHUH&*g8og76tf^&RF5e7%#(&*GBJHG65:}?",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

        # global DB connection across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


