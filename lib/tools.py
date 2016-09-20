import dateparser
import tzlocal
import pytz
import datetime
import lxml

class Tools:
	def __init__(self):
		pass

	@classmethod
	def xpath(self, parent=None, syntax=None):
		assert parent is not None, "Parent is not defined."
		assert syntax is not None, "Syantax is not defined."
		
		if "re:test" in syntax:
			try:
				regexpNS = "http://exslt.org/regular-expressions"
				result   = parent.xpath(syntax,namespaces={'re':regexpNS})
			except lxml.etree.XPathEvalError as invalid_expression:
				print(syntax)
				raise
			except UnicodeDecodeError:
				result = None
		else:
			try:
				result = parent.xpath(syntax)
			except UnicodeDecodeError:
				result = None
		return result