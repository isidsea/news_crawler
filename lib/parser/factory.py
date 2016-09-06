from .article import ArticleParser
from .date    import DateParser

class ParserFactory:
	ARTICLE = 0
	DATE    = 1

	def __init__(self):
		pass

	@classmethod
	def get_parser(self, parser_name=None):
		assert parser_name is not None, "parser_name is not defined."
		if parser_name == ParserFactory.ARTICLE:
			return ArticleParser()
		elif parser_name == ParserFactory.DATE:
			return DateParser()