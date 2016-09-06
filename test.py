from curtsies 			   import fmtstr
from lib.test 			   import Status
from lib.exceptions 	   import NetworkError, ValidationError, ParseError
from lib.validator.factory import ValidatorFactory
from lib.parser.factory    import ParserFactory
from lib.news 			   import News
import glob
import os
import importlib
import random

def print_field(name=None, value=None):
	status = fmtstr(value[0],value[1]) if len(value) > 1 else value[0]
	print("| %s%s| %s%s|" % (
		name, 
		" " * (23-len(name)), 
		status,
		" " * (23-len(value[0]))
	))

def print_status(**kwargs):
	article        = kwargs.get("article", Status.NONE)
	content        = kwargs.get("content", Status.NONE)
	title          = kwargs.get("title", Status.NONE)
	published_date = kwargs.get("published_date", Status.NONE)
	author_name    = kwargs.get("author_name", Status.NONE)
	name 		   = kwargs.get("name", None)

	width = 50
	print("=" * width)
	print_field("NAME", (name,))
	print_field("ARTICLE", article)
	print_field("CONTENT", content)
	print_field("TITLE", title)
	print_field("PUBLISHED_DATE", published_date)
	print_field("AUTHOR_NAME", author_name)
	print("=" * width)

if __name__ == "__main__":
	for file_name in glob.iglob(os.path.join(os.getcwd(),"src","*.py")):
		file_name = file_name.replace(os.getcwd(),"")
		file_name = file_name.replace("src","")
		file_name = file_name.replace(".py","")
		file_name = file_name.replace("/","")
		print("[test][debug] Testing %s" % file_name)

		module  = importlib.import_module("src.%s" % file_name)
		crawler = module.Crawler()

		content_status        = Status.NONE
		title_status          = Status.NONE
		published_date_status = Status.NONE
		author_name_status    = Status.NONE
		article_status 		  = Status.NONE
		test_links            = random.sample(crawler.CATEGORY_LINKS,1 if len(crawler.CATEGORY_LINKS) == 1 else 3)
		try:
			for link in test_links:
				news 			   = News()
				news.url 		   = link
				news.article_xpath = crawler.ARTICLE_XPATH
				articles 		   = news.get_articles()

				if len(articles) == 0:
					article_status = Status.FAILED
					raise AssertionError("Cannot find article! %s" % link.encode("utf-8"))
				article_status = Status.SUCCESS
				article        = random.sample(articles,1)[0]
				print("[test][debug] %s" % article.encode("utf-8"))

				parser = ParserFactory.get_parser(ParserFactory.ARTICLE)
				article = parser.parse(
						       url = article,
						   content = crawler.CONTENT_XPATH,
					published_date = crawler.PUBLISHED_DATE_XPATH,
					         title = crawler.TITLE_XPATH,
					   author_name = crawler.AUTHOR_NAME_XPATH
				)

				content_status    = Status.FAILED
				content_validator = ValidatorFactory.get_validator(ValidatorFactory.CONTENT)
				content_validator.validate(article.content)
				content_status = Status.SUCCESS

				title_status      = Status.FAILED
				content_validator = ValidatorFactory.get_validator(ValidatorFactory.CONTENT)
				content_validator.validate(article.title)
				title_status = Status.SUCCESS

				published_date_status    = Status.FAILED
				pubslihed_date_validator = ValidatorFactory.get_validator(ValidatorFactory.PUBLISHED_DATE)
				pubslihed_date_validator.validate(article.published_date)
				published_date_status = Status.SUCCESS

				author_name_status    = Status.FAILED
				author_name_validator = ValidatorFactory.get_validator(ValidatorFactory.AUTHOR)
				author_name_validator.validate(article.author_name)
				author_name_status = Status.SUCCESS
		except AssertionError as ex:
			print(fmtstr("[test][error] %s" % ex, "red"))
		except NetworkError as ex:
			print(fmtstr("[test][error] %s" % ex, "red"))
		except ValidationError as ex:
			print(fmtstr("[test][error] %s" % ex, "red"))
		except ParseError as ex:
			print(fmtstr("[test][error] %s" % ex, "red"))
		print_status(
				      name = crawler.CRAWLER_NAME,
				   article = article_status,
			       content = content_status,
			         title = title_status,
			published_date = published_date_status,
			   author_name = author_name_status
		)