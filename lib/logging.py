from .database import Database
import arrow

class Logging:

	def __init__(self):
		pass

	@classmethod
	def error(self, **kwargs):
		document = {
			"_insert_time" : arrow.utcnow().datetime,
			       "_type" : "error",
			      "source" : kwargs.get("source", None),
			       "error" : {
				                   "message" : kwargs.get("message", None),
				                 "exception" : kwargs.get("exception", None)
			                 }
		}
		db = Database.get_db()
		db.log.insert_one(document)