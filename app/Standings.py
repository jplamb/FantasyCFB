##########################################
# Standings class manages league standings
# Created by John Lamb
##########################################

from dbConn import *

class Standings:
	
	def __init__(self, team_names):
		self.team_names = team_names
		
		if not check_table_exists("standings"):
			self.create_table("standsings")
	
	def create_table(self, table_name):
		
		open_db_connection()
		
		create_sql = """create table %s
					week int not null
					team varchar(20) not null
					points int not null default 0
					primary key (week, team)
					""" % table_name
		
		