import os
from configparser import ConfigParser

settings = ConfigParser()
settings.read(os.path.abspath(os.path.join(
              os.path.dirname(__file__), "./settings.ini")))
