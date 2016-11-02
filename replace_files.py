import logging
import os 
import re
import sys

from auto_workflow import SqlBase

class ReplaceFiles(SqlBase):

	''' Rapid replace of DB code for specified schemas excluding exclusions
	'''

	def connect(self):

		self.connect_db()

	def run(self):

		self.replace_files()

	def replace_files(self):

		root = os.path.join(self.folders_scripts, 'oracle')

		pattern = r'\b%s\b' % self.replace_from
		prog = re.compile(pattern, re.IGNORECASE)

		logging.info('Replacing instances of %s in files within folder %s with %s' % (self.replace_from, root, self.replace_to))

		for dirpath, dirnames, filenames in os.walk(root):

			for filename in filenames:

				filepath = os.path.join(dirpath, filename)

				# Don't allow the excluded files
				if self.exclusions_prog.search(filepath): continue

				with open(filepath, 'rb') as f:

					fcontent = f.read()

				frcontent = prog.sub(self.replace_to, fcontent)

				if frcontent != fcontent:

					with open(filepath, 'wb') as f:

						f.write(frcontent)

					logging.info('Replaced text in %s' % filepath)

		logging.info('Completed replacing files')


if __name__ == '__main__':

	ReplaceFiles().run()