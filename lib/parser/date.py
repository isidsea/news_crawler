from . 			  import Parser
from ..exceptions import ParseError
import arrow
import dateparser
import tzlocal
import pytz
import datetime
import bson.json_util

class DateParser(Parser):
	def __init__(self):
		Parser.__init__(self)

	@classmethod
	def parse(self, str_date):
		Parser.parse(self)
		assert str_date       is not None, "str_date is not defined."
		assert type(str_date) is str     , "str_date should in str."	

		# manual date conversion
		if "jum'at" in str_date.lower():
			str_date = str_date.lower().replace("jum'at","jumat")
		
		try:
			result = dateparser.parse(str_date)
			if result is None:
				result = arrow.get(str_date).datetime
			if result.tzinfo is None: 
				result = tzlocal.get_localzone().localize(result, is_dst=None)
			result = result.astimezone(pytz.utc)
		except AttributeError as attr_err:
			raise ParseError("Date cannot be parsed. AttributeError (%s)" % str_date)
		except ValueError as value_error:
			raise ParseError("Date cannot be parsed. ValueError (%s)" % str_date)
		except arrow.parser.ParserError:
			raise ParseError("Date cannot be parsed. ArrowError (%s)" % str_date)
		except:
			raise

		if result is not None:
			assert type(result) is datetime.datetime, "result is not datetime."
		return result