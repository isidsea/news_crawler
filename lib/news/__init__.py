from ..database      import Database
from ..network_tools import NetworkTools
from ..tools   	     import Tools
import arrow

class News:
	def __init__(self, **kwargs):
		self.url           = kwargs.get("url",None)
		self.country       = kwargs.get("country",None)
		self.article_xpath = kwargs.get("article_xpath",None)

	# @classmethod
	# def get_active(self):
	# 	db   = Database.get_db()
	#  	news = db.news_list.find({"is_active":True})
	# 	return news

	@classmethod
	def save_to_db(self, document=None):
		assert document is not None, "document is not defined"
		db = Database.get_db()
		db.data.insert_one(document)

	def get_articles(self, xpath=True):
		if xpath:
			assert self.article_xpath is not None, "article_xpath is not defined."
		assert self.url is not None, "url is not defined."

		page     = NetworkTools.parse(self.url)
		articles = Tools.xpath(page, self.article_xpath)
		articles = list(set(articles))
		articles = [NetworkTools.full_url(self.url, url) for url in articles]
		return articles

	def build_document(self, article=None):
		assert article      is not None, "article is not defined."
		assert self.url     is not None, "url is not defined."
		assert self.country is not None, "country is not defined."

		document = {}
		document.update({"_insert_time" : arrow.utcnow().datetime})
		document.update({"_crawled_by" : "News Crawler"})
		document.update({"permalink" : article.permalink})
		document.update({"title" : article.title})
		document.update({"author_name" : article.author_name})
		document.update({"content" : article.content})
		document.update({"published_date" : article.published_date})
		document.update({"origin" : self.url})
		document.update({"_country" : self.country})
		document.update({"domain" : NetworkTools.get_domain(article.permalink, with_scheme=False)})
		document.update({"converted" : False})
		return document