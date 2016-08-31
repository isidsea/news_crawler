from . import Config
import os

class ConverterConfig(Config):
	def __init__(self):
		Config.__init__(self, os.path.join(".","config","converter.json"))