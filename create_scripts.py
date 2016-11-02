import logging
import os 
import re

import sys

from sqlbase import SqlBase

class CreateScripts(SqlBase):

	''' Create the code base '''

	def connect(self):

		self.connect_db()

	def run(self):

		self.write_files()

	def write_files(self):

		allowed_schemas = [x.upper() for x in self.db_allowed_schemas.split(',')]

		SQL_1 = """ select owner, name, type, line, text
				      from all_source
				     where owner in ( '%s' )
				     order by owner, name, type, line
			    """ % "','".join(allowed_schemas)

		# Cannot combine these queries in SQL due to LONG datatype
		SQL_2 = """ select owner, view_name, 'VIEW', 1, text
  				      from all_views
				     where owner in ( '%s' )
				     order by owner, view_name
				""" % "','".join(allowed_schemas)

		# SQL for tables
		SQL_3 = """ select owner, table_name, 'TABLE', 1
     					 , dbms_metadata.get_ddl('TABLE', table_name, owner)
  				      from all_tables
				     where owner in ( '%s' )
				     order by owner, table_name
				""" % "','".join(allowed_schemas)

		SQLs = [SQL_1, SQL_2, SQL_3]

		for SQL in SQLs:

			self.cur.execute(SQL)

			owner = ''
			name = ''
			object_type = ''
			bad_name = ''

			for row in self.cur:

				to_compile = row[4]

				if row[0] != owner or row[1] != name or row[2] != object_type:

					owner = row[0] ; name = row[1] ; object_type = row[2]
					
					try:
						to_compile = re.sub(r'^%s\s+%s' % (object_type, name), 'create or replace %s %s.%s' % (object_type, owner, name), to_compile, flags=re.IGNORECASE)
					except TypeError:
						pass

					print object_type, owner, name

					if object_type == 'PACKAGE BODY':
						object_type_folder = 'package'
						ext = '.pkb'
					elif object_type == 'PACKAGE':
						object_type_folder = 'package'
						ext = '.pks'
					elif object_type == 'TYPE BODY':
						object_type_folder = 'type'
						ext = '.tpb'
					elif object_type == 'TYPE':
						object_type_folder = 'type'
						ext = '.tps'
					elif object_type == 'JAVA SOURCE':
						object_type_folder = 'java'
						ext = '.sql'
					else:
						object_type_folder = object_type.lower()
						ext = '.sql'

					path = os.path.join(self.folders_scripts, 'oracle', owner.lower(), object_type_folder)

					try:
						os.makedirs(path)
					except WindowsError:
						pass

					filename = name.lower() + ext

					try:
						f.close()
					except NameError:
						pass

					try:
						f = open(os.path.join(path, filename), 'w')
					except IOError:
						bad_name = name
						continue

					logging.debug(os.path.join(path, filename))

				if name == bad_name:
					continue

				if object_type == 'JAVA SOURCE':
					f.write(to_compile or '' + '\r\n')
				elif object_type == 'VIEW':
					f.write('create or replace view %s.%s as \r\n%s' % (owner, name, row[4]))
				elif object_type == 'TABLE':
					f.write(row[4].read())
				else:
					f.write(to_compile)

			f.close()

		logging.info('Completed')


if __name__ == '__main__':

	CreateScripts().run()