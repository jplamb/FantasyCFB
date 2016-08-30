########################################
# Roster class defines a person's roster
# Created by John Lamb
########################################

from dbConn import *

class Roster:
	
	# init creates table and adds players to roster table
	# inputs: team name as string, team_players as list
	def __init__(self, team_name):
		self.team_name = team_name
		self.team_players = self.get_team_players() 
		self.table_name = team_name
		
		if not check_table_exists(table_name):
			self.create_team_roster(self.table_name)
		
		#update_roster_players(team_players)
	
	# create roster table
	def create_team_roster(self):
						
		create_string = """ create table %s
				week int not null,
				player_name varchar(20) not null,
				pos varchar(2),
				starting varchar(1) not null,
				points_elig varchar(1) not null,
				points float,
				opp varchar(20)
				primary key (week, player_name
				)""" % self.table_name
		
		db_execute(create_string)
	
	# interface with google sheet to pull in roster
	def get_team_players():
		#players = []
		pass
		# self.update_roster(players, week)
		#return players
	
	# Delete all rows and add players, set elig and start to 'N'
	# inputs: team players as list (not attribute of class in case called externally
	def update_roster(self, players, week):
		delete_sql = """
			delete from %s
			where week = %s
			""" %(self.table_name, week)
		
		db_execute(delete_sql)
		
		for player in players:
			# check_row_sql = """
			# 	select (1) from %s
			# 	where week = %s
			# 	and player = '%s'
			# 	""" %(self.table_name, week, player)
			# if db_execute(check_row_sql):
				#self.update_player(player, week)
			#else:
			self.insert_player(player, week)
	
	def update_roster_stats(self, week):
		for player in self.team_players:
			pass
		# get latest game log
		# run sql to update current stats
	
	def update_player(self, player, week, points_elig, pos, starting, opp):
		update_sql = """
				update %s set
				points_elig = '%s',
				pos = '%s',
				starting = '%s',
				opp = '%s'
				where week = %s
				and player = '%s'
				""" %(self.table_name, points_elig, pos, starting, opp, week, player)

		db_execute(update_sql)
	
	def insert_player(self, player, week, points_elig, pos, starting, opp):
		insert_sql = """
				insert into %s
				(week, player, points_elig, points, pos, starting, opp)
				values
				(%s, '%s', '%s', 0, '%s', '%s', '%s')
				"""%(self.table_name, week, player, points_elig, pos, starting, opp)
				
		db_execute(insert_sql)

			


		
		
	
		
		
		