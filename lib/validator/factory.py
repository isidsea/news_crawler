from .content 		 import ContentValidator
from .published_date import PublishedDateValidator
from .author         import AuthorValidator

class ValidatorFactory:
	CONTENT    	   = 0
	PUBLISHED_DATE = 1
	AUTHOR         = 2

	def __init__(self):
		pass

	@classmethod
	def get_validator(self, validator_name=None):
		assert validator_name is not None, "validator_name is not defined."

		if validator_name == ValidatorFactory.CONTENT:
			return ContentValidator()
		elif validator_name == ValidatorFactory.PUBLISHED_DATE:
			return PublishedDateValidator()
		elif validator_name == ValidatorFactory.AUTHOR:
			return AuthorValidator()