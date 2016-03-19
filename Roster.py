########################################
# Roster class defines a person's roster
# Created by John Lamb
########################################

from dbConn import *

class Roster:
	
	def __init__(self, team_name,team_players):
		self.team_name = team_name
		self.team_players = team_players
		
		if not check_table_exists(team_name):
			self.create_team_roster(self.team_name)
	
	def create_team_roster(self, table_name):
		
		table_name =  "_".join(name.lower().split(" "))
		
		open_db_connection()
		
		create_string = """ create table %s
				player varchar(20) not null
				pos varchar(2) not null
				starting varchar(1) not null
				elig varchar(1) not null
				opp varchar(20)""" % table_name
		
		cursor.execute(create_string)
		
		close_db()

	def update_roster_players(self, team_players):
		print ""
		
	def update_opps(self):
		print ""
		
	def update_starters(self):
		print ""