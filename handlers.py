import tornado.web
from tornado.escape import json_encode
from tornado import httpclient, gen
from bs4 import BeautifulSoup
import re
from collections import Counter
from random import shuffle

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")


class ScrapeHandler(BaseHandler):

	def get_words(self, text):
		return re.compile('\w+').findall(text)

	@gen.coroutine
	def get_words_from_url(self, url):

		try:
			response = yield httpclient.AsyncHTTPClient().fetch(url)
			html = response.body if isinstance(response.body, str) else response.body.decode()

			# parse the html to get cleaned text
			soup = BeautifulSoup(html, 'html.parser')
			for s in soup(['script', 'style', 'head', 'title', '[document]']):
				s.extract()

			# extract all words
			words = self.get_words( soup.get_text().lower() )

			c = Counter(words).most_common(100)

			# save the top 100 words in DB


		except Exception as e:
			print('Exception: %s %s' % (str(e), url))
			raise gen.Return([])

		raise gen.Return(c)

	@gen.coroutine
	def post(self):

		url = self.get_argument("url")

		words = yield self.get_words_from_url(url)

		self.write(json_encode({"result": words}))
