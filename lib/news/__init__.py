from ..database import Database
from .engine    import Engine

class News:
	def __init__(self, **kwargs):
		self.url     = kwargs.get("url",None)
		self.country = kwargs.get("country",None)

	@classmethod
	def get_active(self):
		db   = Database.get_db()
		news = db.news_list.find({"is_active":True})
		return news