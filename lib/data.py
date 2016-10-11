from .database import Database

class Data:
	def __init__(self):
		pass

	@classmethod
	def get_not_converted(self):
		print("[data][debug] Getting not converted...")
		db = Database.get_db()
		return db.data.find({"$or":[{"converted":False}, {"converted":None}]})