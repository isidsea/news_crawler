from . import Config
import os

class RunConfig(Config):
	def __init__(self):
		Config.__init__(self, os.path.join(".","config","run.json"))