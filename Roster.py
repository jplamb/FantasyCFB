########################################
# Roster class defines a person's roster
# Created by John Lamb
########################################

from dbConn import *

class Roster:
	
	# init creates table and adds players to roster table
	# inputs: team name as string, team_players as list
	def __init__(self, team_name,team_players):
		self.team_name = team_name
		self.team_players = team_players
		self.table_name = "_".join(name.lower().split(" "))
		
		if not check_table_exists(table_name):
			self.create_team_roster(self.table_name)
		
		update_roster_players(team_players)
	
	# create roster table
	def create_team_roster(self):
				
		open_db_connection()
		
		create_string = """ create table %s
				player varchar(20) not null
				pos varchar(2)
				starting varchar(1) not null
				elig varchar(1) not null
				opp varchar(20)""" % self.table_name
		
		cursor.execute(create_string)
		
		close_db()
	
	# Delete all rows and add players, set elig and start to 'N'
	# inputs: team players as list (not attribute of class in case called externally
	def update_roster_players(self, team_players):
		
		open_db_connection()
		
		truncate_sql = """truncate %s
					""" % self.table_name
		
		insert_sql = """
				insert into %s
				(player, starting, elig)
				values
				('%s', 'N', 'N')
				""" 
		for player in team_players:
			sql = insert_sql % (self.table_name, player)
			cursor.execute(sql)
		
		close_db()
	
	# Get schedule details and update opp, then update eligibility
	def update_opps(self):
		print ""
		
	# Update player starting status
	# inputs: Player_starts as 2D list (player, status)
	def update_starters(self, player_starts):
		
		open_db_connection()
		
		update_sql = """
				update %s
				set status = '%s'
				where player = '%s'
				"""
		
		for player in player_starts:
			sql = update_sql % (self.table_name, player[1], player[2])
			cursor.execute(sql)
		
		close_db()
		
	
		
		
		