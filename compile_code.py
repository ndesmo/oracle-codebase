import logging
import sys
import os

from sqlbase import SqlBase

class CompileCode(SqlBase):

	''' Compile specified objects '''

	def connect(self):

		self.connect_db()

	def run(self):

		self.compile_code()


	def compile_code(self):

		''' Compile the objects of given type and schema back to the db '''

		compile_schemas = self.compile_schemas.split(',')
		compile_types = self.compile_types.split(',')

		root = os.path.join(self.folders_scripts, 'oracle')

		for schema in compile_schemas:

			for typ in compile_types:

				dirpath = os.path.join(root, schema, typ)

				try:

					for filename in [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]:

						filepath = os.path.join(dirpath, filename)

						# Don't allow the excluded files
						if self.exclusions_prog.search(filepath): continue

						with open(filepath, 'r') as f:

							SQL = f.read()

							print filepath

							try:
								self.cur.execute(SQL)
								logging.debug('Compiled %s.%s' % (schema, filename))
							except:
								logging.error('Could not complile %s.%s' % (schema, filename))

				except WindowsError:
					pass

		logging.info('Finished compiling code')


if __name__ == '__main__':

	CompileCode().run()