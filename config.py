import os
import tornado.web
import torndb
from tornado.options import define, options
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import MySQLdb

from handlers import HomeHandler, ScrapeHandler, AdminHandler



define("port", default=8000, help="run on the given port", type=int)

define("mysql_host", default="127.0.0.1:3306")
define("mysql_database", default="wordcount")
define("mysql_user", default="wordcount")
define("mysql_password", default="12345678")

define("cookie_secret", default="87t7868&T^&RHUH&*g8og76tf^&RF5e7%#(&*GBJHG65:}?")
define("words_pk_salt", default="L})usq/7$X?Ef Cl-9[F+q/)8vkv,Fm^9=:xdb`*@9C>N[]:}es_w?._*|EC.~Wk")
define("key_file_pass", default = b'*7K7zv4=8Yh#THm?6WU+')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/scrape/", ScrapeHandler),
            (r"/admin/", AdminHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret=options.cookie_secret,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

        # global DB connection across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        #
        # create database if required
        #
        try:
            self.db.get('SELECT COUNT(*) from `words`;')

        except MySQLdb.ProgrammingError: 

            with open('database.sql', 'r') as schema:
                self.db.execute( schema.read() )
                self.db.reconnect()


        self.words_pk_salt = options.words_pk_salt

        #
        # load the private key
        #
        if not os.path.isfile('key.pem'):  

            # key file not generated, generate one now        
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(options.key_file_pass)
            )

            # save the generated key
            with open('key.pem', 'w') as key_file:
                key_file.writelines("%s\n" % l for l in pem.splitlines())

        with open("key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=options.key_file_pass,
                backend=default_backend()
            )

            self.public_key = self.private_key.public_key()

