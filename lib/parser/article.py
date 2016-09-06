from ..network_tools    import NetworkTools
from ..tools   			import Tools
from ..cleanser.factory import CleanserFactory
from ..news.article     import Article
from ..exceptions 		import NetworkError, ParseError
from .date 			    import DateParser
from . 					import Parser

class ArticleParser(Parser):
	def __init__(self):
		Parser.__init__(self)

	def parse(self, **kwargs):
		try:
			Parser.parse(self)

			title          = kwargs.get("title", None)
			content        = kwargs.get("content", None)
			published_date = kwargs.get("published_date", None)
			author_name    = kwargs.get("author_name", None)
			url            = kwargs.get("url", None)

			assert title          is not None, "title is not defined."
			assert content        is not None, "content is not defined."
			assert published_date is not None, "published_date is not defined."
			assert author_name    is not None, "author_name is not defined."
			assert url            is not None, "url is not defined."

			page           = NetworkTools.parse(url)
			title          = Tools.xpath(page, title)
			title 		   = "".join(title)
			content        = Tools.xpath(page, content)
			content  	   = "".join(content)
			published_date = Tools.xpath(page, published_date)
			published_date = "".join(published_date)
			author_name    = Tools.xpath(page, author_name)
			author_name    = "".join(author_name)

			cleanser       = CleanserFactory.get_cleanser(CleanserFactory.STRING)
			title          = cleanser.clean(title)
			content        = cleanser.clean(content)
			published_date = cleanser.clean(published_date)
			author_name    = cleanser.clean(author_name)
			
			date_parser    = DateParser()
			published_date = date_parser.parse(published_date)

			return Article(
				         title = title,
				       content = content,
				published_date = published_date,
				   author_name = author_name,
				     permalink = url
			)
		except NetworkError as ex:
			raise ParseError("%s" % ex)