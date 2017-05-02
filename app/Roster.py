########################################
# Roster class defines a person's roster
# Created by John Lamb
########################################

from dbConn import Mysql
from gSheet import get_values

class Roster:
	
	# init creates table and adds players to roster table
	# inputs: team name as string, team_players as list
	def __init__(self, team_name):
		self.team_name = team_name
		self.team_players_strt  = self.get_team_players(True)
		self.team_players_bnch = self.get_team_players(False)
		#self.table_name = team_name.replace(' ', '_')
		self.table_name = 'roster'
		
		self.conn = Mysql()
		
		table_exists = self.conn.call_store_procedure('check_table_exists', self.table_name)
		
		if not table_exists:
			self.conn.call_store_procedure('create_roster')
	
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
		delete_where = "week = %s and fant_team = '%s'" %(week, self.team_name)
		self.conn.delete(self.table_name, delete_where)
		
		for player in self.team_players_strt:
			self.insert_player(week, True, player)
		for player in self.team_players_bnch:
			self.insert_player(week, False, player)
	
	# Add players to table
	def insert_player(self, week, start, *player):
		table_values = {}
		player = player[0]
		
		pos = player[0]
		table_values['week'] = week
		table_values['fant_team'] = self.team_name		
		table_values['pos'] = pos
		table_values['player_name'] = player[1]
		table_values['points_elig'] = player[4][0]
		table_values['team'] = player[2]
		table_values['opp'] = player[3]
		table_values['points'] = 0

		if start:
			table_values['is_starting'] = 'Y'
		else:
			table_values['is_starting'] = 'N'
			
		if pos.lower() == 'kicker':
			table_values['pos'] = 'PK'
		if pos.lower() == 'defense':
			table_values['pos'] = 'D'
		
		self.conn.insert(self.table_name, **table_values)
			


		
		
	
		
		
		