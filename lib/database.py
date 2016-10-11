import pymongo

class Database:
	def __init__(self):
		pass

	@classmethod
	def get_db(self):
		conn = pymongo.MongoClient("mongodb://mongo:27017")
		db   = conn["news_crawler"]

		# Ensuring Indexes
		db.data.create_index([("permalink", pymongo.ASCENDING)], unique=True)
		db.data.create_index([("converted", pymongo.ASCENDING)])
		db.failed_urls.create_index([("permalink", pymongo.ASCENDING)], unique=True)
		return db