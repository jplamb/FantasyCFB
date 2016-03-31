########################################################
#  Common database connection actions
#  3/13/16  John Lamb
########################################################

import base64
import MySQLdb

# open db connection to ffbdev
def open_db_connection():
	global db
	global cursor
	db = MySQLdb.connect('localhost', 'appuser', base64.b64decode('YXBwdXNlcg=='), 'ffbdev')
	
	cursor = db.cursor()
	
# close db connection to ffbdev and commit
def close_db():
	db.commit()
	db.close()
	
# check if table exists
# Inputs: player table name
# Returns boolean if table exists
def check_table_exists(name):
	open_db_connection()
		
	show = 'show tables like \'%s\'' % name
	result = cursor.execute(show)
		
	if result:
		close_db()
		return True
		
	close_db()
	return False

def execute_sql(sql):
	cursor.execute(sql)