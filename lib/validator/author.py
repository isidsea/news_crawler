from .            import Validator
from ..exceptions import ValidationError

class AuthorValidator(Validator):
	def __init__(self):
		Validator.__init__(self)

	def validate(self, content=None):
		Validator.validate(self, content)

		if not content: raise ValidationError("Author cannot be empty.")
		return content

	