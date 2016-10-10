########################################################
#  Common database connection actions
#  3/13/16  John Lamb
########################################################

import base64
import MySQLdb
import os
# open db connection to ffbdev
def open_db_connection(dict):
	global db
	global cursor
	
	db = MySQLdb.connect('localhost', 'appuser', base64.b64decode('YXBwdXNlcg=='), 'ffbdev')

	if not dict:
		cursor = db.cursor()
	else:
		cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	
# close db connection to ffbdev and commit
def close_db():
	db.commit()
	db.close()
	
# check if table exists
# Inputs: player table name
# Returns boolean if table exists
def check_table_exists(name):
	#open_db_connection(False)
	show = 'show tables like \'%s\'' % name
	result = cursor.execute(show)
		
	if result:
		#close_db()
		return True
		
	#close_db()
	return False

def execute_sql(sql):
	cursor.execute(sql)
	
# mask db operations
def db_execute(sql):
	#open_db_connection(False)
	
	execute_sql(sql)
	result = cursor.fetchall()
	
	#close_db()
	
	return result

# retrieve results as dict
def db_dict_execute(sql):
	#open_db_connection(True)
	cursordict = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	cursordict.execute(sql)
	result = cursordict.fetchall()
	
	cursordict.close()
	#close_db()
	
	return result

def db_commit():
	db.commit()

#class MySqlCursorDict(mysql.connector.cursor.MySQLCursor):
#	def _row_to_python(self, rowdata, desc=None):
#		row = super(MySqlCursorDict, self)._row_to_python(rowdata, desc)
#		if row:
#			return dict(zip(self.column_names, row))
#		return None