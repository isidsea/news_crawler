from .converter import ConverterConfig
from .run   	import RunConfig

class ConfigFactory:
	CONVERTER = 0
	RUN       = 1

	def __init__(self):
		pass

	@classmethod
	def get(self, config_name=None):
		assert config_name is not None, "config_name is not defined."
		if config_name == ConfigFactory.CONVERTER:
			return ConverterConfig()
		elif config_name == ConfigFactory.RUN:
			return RunConfig()

