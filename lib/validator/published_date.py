from .            import Validator
from ..exceptions import ValidationError
import arrow
import pytz

class PublishedDateValidator(Validator):
	def __init__(self):
		Validator.__init__(self)

	def validate(self, date=None):
		try:
			assert date is not None, "date is not defined"
			Validator.validate(self, date)
			if date.replace(tzinfo=pytz.UTC) > arrow.now().replace(days=1).datetime.replace(tzinfo=pytz.UTC):
				raise ValidationError("Future date!")
		except AssertionError:
			raise ValidationError("No published_date!")