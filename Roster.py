########################################
# Roster class defines a person's roster
# Created by John Lamb
########################################

from dbConn import *
from gSheet import get_values

class Roster:
	
	# init creates table and adds players to roster table
	# inputs: team name as string, team_players as list
	def __init__(self, team_name):
		self.team_name = team_name
		self.team_players_strt  = self.get_team_players(True)
		self.team_players_bnch = self.get_team_players(False)
		self.table_name = team_name.replace(' ', '_')
		
		if not check_table_exists(self.table_name):
			self.create_team_roster()
		
		#update_roster_players(team_players)
	
	# create roster table
	def create_team_roster(self):
		
		create_string = """ create table %s (
				week int not null,
				player_name varchar(20) not null,
				pos varchar(2),
				is_starting varchar(1) not null,
				points_elig varchar(1) not null,
				points float,
				team varchar(20),
				opp varchar(20),
				primary key (week, player_name)
				)""" % self.table_name
		db_execute(create_string)
	
	# interface with google sheet to pull in roster
	def get_team_players(self, starters):
		if starters:
			range = self.team_name.replace(' ', ' - ',1) + '!A3:E8'
		else:
			range = self.team_name.replace(' ', ' - ',1) + '!A11:E15'
		players = get_values(range)
		return players
	
	# Delete all rows and add players, set elig and start to 'N'
	# inputs: team players as list (not attribute of class in case called externally
	def update_roster(self, week):
		delete_sql = """
			delete from %s
			where week = %s
			""" %(self.table_name, week)
		
		db_execute(delete_sql)
		
		for player in self.team_players_strt:
			self.insert_player(week, True, player)
		for player in self.team_players_bnch:
			self.insert_player(week, False, player)
	
	def update_roster_stats(self, week):
		for player in self.team_players:
			pass
		# get latest game log
		# run sql to update current stats
	
	def insert_player(self, week, start, *player):
		player = player[0]
		
		pos = player[0]
		player_nm = player[1]
		team = player[2]
		opp = player[3]
		points_elig = player[4][0]

		if start:
			starting = 'Y'
		else:
			starting = 'N'
			
		if pos.lower() == 'kicker':
			pos = 'PK'
		if pos.lower() == 'defense':
			pos = 'D'
			
		insert_sql = """
				insert into %s
				(week, player_name, points_elig, points, pos, is_starting, team, opp)
				values
				(%s, '%s', '%s', 0, '%s', '%s', '%s','%s')
				"""%(self.table_name, week, player_nm, points_elig,  pos, starting, team, opp)
		db_execute(insert_sql)

			


		
		
	
		
		
		