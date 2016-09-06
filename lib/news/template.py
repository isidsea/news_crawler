import os

class Template:
	TEMPLATE             = os.path.join(os.getcwd(), "templates", "news_crawler.arct")
	CRAWLER_NAME   		 = ""
	COUNTRY              = ""
	CATEGORY_LINKS 		 = []
	ARTICLE_XPATH  		 = ""
	TITLE_XPATH    		 = ""
	PUBLISHED_DATE_XPATH = ""
	AUTHOR_NAME_XPATH    = ""
	CONTENT_XPATH 		 = ""