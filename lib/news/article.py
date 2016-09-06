class Article:
	def __init__(self, **kwargs):
		self.permalink      = kwargs.get("permalink", None)
		self.content        = kwargs.get("content", None)
		self.title          = kwargs.get("title", None)
		self.author_name    = kwargs.get("author_name", None)
		self.published_date = kwargs.get("published_date", None)

		self.content_xpath        = kwargs.get("content_xpath", None)
		self.title_xpath 		  = kwargs.get("title_xpath", None)
		self.author_name_xpath    = kwargs.get("author_name_xpath", None)
		self.published_date_xpath = kwargs.get("published_date_xpath", None)