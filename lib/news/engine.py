from ..network_tools     import NetworkTools
from ..validator.factory import ValidatorFactory
from ..exceptions        import ValidationError, ParseError, NoHTML
from ..database          import Database
from curtsies            import fmtstr
import pymongo
import newspaper
import copy
import arrow
import lxml
import socket

class Engine:
	def __init__(self):
		pass

	def crawl(self, news=None):
		assert news     is not None, "news is not defined."
		assert news.url is not None, "news.url is not defined."

		self.news = copy.deepcopy(news)
		print("[news_engine][debug] Crawling: %s" % news.url)

		articles = self.get_articles(news)
		print("[news_engine][debug] Got %s article(s)" % len(articles))

		for article in articles:
			try:
				print("[news_engine][debug] Parsing: %s" % article.url.encode("utf-8"))
				document = self.build_document(article)

				print("[news_engine][debug] Validating...")
				validator = ValidatorFactory.get_validator(ValidatorFactory.CONTENT)
				validator.validate(document["content"])

				validator = ValidatorFactory.get_validator(ValidatorFactory.PUBLISHED_DATE)
				validator.validate(document["published_date"])

				print("[news_engine][debug] Inserting to DB...")
				db = Database.get_db()
				db.data.insert_one(document)
			except ValidationError as ex:
				print(fmtstr("[news_engine][error] %s" % ex, "red"))
			except ParseError as ex:
				print(fmtstr("[news_engine][error] %s" % ex, "red"))
			except pymongo.errors.DuplicateKeyError:
				print(fmtstr("[news_engine][error] Duplicate Document!","red"))

	def build_document(self, article=None):
		assert article   is not None, "article is not defined."
		assert self.news is not None, "news is not defined."
		success = False
		max_try = 2
		tried   = 0
		while not success and tried < max_try:
			try:
				article.download()
				article.parse()
				success = True
			except newspaper.article.ArticleException:
				print(fmtstr("[news_engine][error] Download overlap error. Trying again...","red"))
			except NoHTML as ex:
				print(fmtstr("[news_engine][error] %s" % ex,"red"))
			except socket.timeout:
				print(fmtstr("[news_engine][error] Connection Timeout","red"))
			except lxml.etree.XMLSyntaxError:
				print(fmtstr("[news_engine][error] lxml parse error.","red"))
			finally:
				tried = tried + 1
		if not success: raise ParseError("Cannot parse article!")

		document = {}
		document.update({"_insert_time" : arrow.utcnow().datetime})
		document.update({"_crawled_by" : "News Crawler"})
		document.update({"permalink" : article.url})
		document.update({"title" : article.title})
		document.update({"author_name" : article.authors[0] if len(article.authors) > 0 else ""})
		document.update({"content" : article.text})
		document.update({"published_date" : article.publish_date})
		document.update({"origin" : self.news.url})
		document.update({"_country" : self.news.country})
		document.update({"domain" : NetworkTools.get_domain(article.url)})
		document.update({"converted" : False})
		return document


	def get_articles(self, news=None):
		assert news     is not None, "news is not defined."
		assert news.url is not None, "news.url is not defined." 

		url      = copy.copy(news.url)
		url      = NetworkTools.full_url(url)
		paper    = newspaper.build(url, memoize_articles=False)
		articles = copy.deepcopy(paper.articles)
		return articles