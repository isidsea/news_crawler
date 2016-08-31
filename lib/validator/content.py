from .            import Validator
from ..exceptions import ValidationError

class ContentValidator(Validator):
	def __init__(self):
		Validator.__init__(self)

	def validate(self, content=None):
		Validator.validate(self, content)

		if not content: raise ValidationError("Content cannot be empty.")

	