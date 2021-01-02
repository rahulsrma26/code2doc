import os

PROGRAM_NAME = 'code2doc'
THIS_DIR = os.path.dirname(__file__)
VERSION = open(os.path.join(THIS_DIR, '__version__.py')).readline()
README = 'ReadMe'
OUTPUT_EXT = '.md'
CONFIG_EXT = '.ini'
DEFAULT_CONFIG_FILENAME = PROGRAM_NAME + CONFIG_EXT