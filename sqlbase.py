import ConfigParser
import cx_Oracle
import logging
import time
import os
import re

class SqlBase:

	''' Base class for connecting and setup of scripts
	'''

	def __init__(self, **kwargs):

		self.config_file = 'settings.ini'
		self.parse_config()

		self.__dict__.update(kwargs)
		self.setup_logging()

		self.connect()
		self.load_exclusions()

	def parse_config(self):

		config = ConfigParser.ConfigParser()
		config.read(self.config_file)

		for row in config._sections.itervalues():
			self.__dict__.update(dict(('%s_%s' % (row['__name__'], x) ,row[x]) for x in row if x != '__name__'))

	def setup_logging(self):

		try:
			os.makedirs(self.folders_logs)
		except WindowsError:
			pass

		log_file = os.path.join(os.path.abspath(self.folders_logs),
								'%s_%s.log' % ( time.strftime('%Y%m%d_%H%M',
											       time.gmtime(time.time())),
												self.__class__.__name__) )

		logging.getLogger('').handlers = []
		logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_file)

	def connect(self):
		pass

	def connect_db(self):

		self.conn = cx_Oracle.connect('%s/%s@%s' % (self.db_schema, self.db_pass, self.db_server))

		self.cur = self.conn.cursor()

		logging.info('Connected to Oracle')

	def load_exclusions(self):

		with open(self.replace_exclusions_file, 'r') as f:
			exclusions = [x.strip() for x in f]

		exclusions_patterns = []

		for exclusion in exclusions:
			schema, obj = exclusion.split('.')
			exclusions_patterns.append(r'%s\\.+?\\%s\.[a-z]+$' % (schema, obj))

		exclusions_pattern = '|'.join(exclusions_patterns)
		self.exclusions_prog = re.compile(exclusions_pattern, re.IGNORECASE)

