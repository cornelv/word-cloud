import tornado.web
from tornado.escape import json_encode
from tornado import httpclient, gen
from bs4 import BeautifulSoup
import re
from collections import Counter
import base64, hashlib

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def encrypt_word(self, word):

    	return self.application.public_key.encrypt(
				str(word),
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA1()),
					algorithm=hashes.SHA1(),
					label=None
				)
			)

    def decrypt_word(self, word):

    	return self.application.private_key.decrypt(
    			word,
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA1()),
					algorithm=hashes.SHA1(),
					label=None
				)
    		)


class AdminHandler(BaseHandler):

	def get(self):
		entries = self.db.query("SELECT word, count FROM words order by count DESC LIMIT 2000;")

		words = []

		for word in entries:
			words.append( (self.decrypt_word(word['word']) , word['count'])) 

		self.render("admin.html", words=words)

class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.html")


class ScrapeHandler(BaseHandler):

	def get_words(self, text):
		return re.compile('\w+').findall(text)

	def save_words(self, words):
		for word in words:

			# generate the primary key
			pk = hashlib.sha512(self.application.words_pk_salt + word[0]).digest()
			pk = base64.urlsafe_b64encode(pk)

			# update the word in DB
			result = self.db.get("SELECT count(id) as cnt FROM `words` WHERE id = %s", pk) # this should be async

			if result['cnt'] > 0:
				# update the count in database
				self.db.execute("UPDATE words set count = count + %s WHERE id = %s;", int(word[1]), pk)

			else:
				# save the new record in Db
				result = self.db.execute("INSERT INTO words (id, word, count) VALUES (%s, %s, %s);", \
										 pk, self.encrypt_word(word[0]), int(word[1]) )

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
			self.save_words(c)


		except Exception as e:
			print('Exception: %s %s' % (str(e), url))
			raise gen.Return([])

		raise gen.Return(c)

	@gen.coroutine
	def post(self):

		url = self.get_argument("url")

		words = yield self.get_words_from_url(url)

		self.write(json_encode({"result": words}))
