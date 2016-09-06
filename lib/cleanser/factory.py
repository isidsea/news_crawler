from .string import StringCleanser

class CleanserFactory:
	STRING = 0

	def __init__(self):
		pass

	@classmethod
	def get_cleanser(self, cleanser_name=None):
		assert cleanser_name is not None, "cleanser_name is not defined."

		if cleanser_name == CleanserFactory.STRING:
			return StringCleanser()