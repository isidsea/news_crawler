from . import Cleanser
import copy

class StringCleanser(Cleanser):
	def __init__(self):
		Cleanser.__init__(self)

	def clean(self, obj=None):
		Cleanser.clean(self, obj)
		assert type(obj) is str, "incorrect obj data type"

		obj = copy.copy(obj)
		obj = obj.replace("\n","")
		obj = obj.replace("\t","")

		return obj