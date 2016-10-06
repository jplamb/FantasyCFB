#####################################################
#  Player class handles data saving for each player
#  Interfaces with mysql db
#  Created by John Lamb
#####################################################

import MySQLdb
import base64
from dbConn import *
from datetime import datetime

# Player class interfaces with database to retrieve and store data
class Player:
	
	#table_name = ""
	
	# init...creates player's stats table if none exists
	def __init__(self, name, ID, url):
		self.name = name
		self.ID = ID
		self.url = url
		
		#self.table_name = "_".join(name.lower().split(" "))
		self.table_name = "player_stats"
		
		# Create data table if it doesn't exist
		if not check_table_exists(self.table_name):
			self.create_player_stats_table(self.table_name)
		# For testing purposes
		"""
		else:
			self.open_db_connection()
			sql = "drop table %s" % self.table_name
			cursor.execute(sql)
			self.create_player_stats_table(self.table_name)
		"""
				
	# Insert or Update rows of gamelog into db
	# Input: player's gamelog
	# Returns: 
	def set_stats(self, stats):
		# Make sure the table exists first
		if not check_table_exists(self.table_name):
			self.create_player_stats_table(self.table_name)			
		
		# Loop through each row in the gamelog 
		#for row in range(1,len(gamelog)):
		for game in range(len(stats['date'])):

			#week = gamelog[row][0]
			week = stats['date'][game]
			week = self.getWeek(week)

			# SQL to check if row already exists in db
			row_check = """select (1)
						from player_stats 
						where player_id = %s and 
						week = %s """
						
			# Execute row check
			row_check = row_check % (self.ID, week)
			
			# Set update/insert base sql strings
			if db_execute(row_check):
				self.update_game_row(stats, week, game)
			else:
				self.insert_game_row(stats, week, game)
					
	def update_game_row(self, stats, week, game):
		update_sql = """update %s set """ % self.table_name
		
		for cat in stats.keys():
			
			update_sql += self.get_corres_col_name(cat) + '='
			stat = stats[cat][game]
			
			if isinstance(stat, float):
				update_sql += "%s," % str(stat)
			else:
				stat = str(stat).translate(None, "'_")
				update_sql += "'%s'," % stat
		update_sql = update_sql[:-1] + "where week = %s and player_id = %s" %(week, self.ID)
		print update_sql
		db_execute(update_sql)
	
	def insert_game_row(self, stats, week, game):
		# Base string for insert statement
		insert_sql_cols = 'insert into %s (player_id, player_name, week,' % self.table_name

		# Generate insert statement base with columns
		for cat in stats.keys():
			insert_sql_cols += self.get_corres_col_name(cat) + ','
		insert_sql_cols = insert_sql_cols[:-1] + """) values (%s, '%s', %s, """ %(self.ID, self.name, week)
		
		for cat in stats.keys():
			stat = stats[cat][game]
			
			if isinstance(stat, float):
				insert_sql += str(stat) + ','
			else:
				stat = str(stat).translate(None, "'_")
				insert_sql += "'%s'," % stat
		
		insert_sql = insert_sql[:-1] + ')'
		db_execute(insert_sql)
			
			# If already in db, run update
			#if db_execute(row_check):
			#	for count, stat in enumerate(gamelog[row]):
			#		update_sql += self.get_corres_col_name(str(gamelog[0][count]).replace(" ","_").lower()) + '='
					
					# Make sure string type columns take in data as string format
			#		if isinstance(stat, basestring):
			#			stat = str(stat).translate(None, "',_")
			#			update_sql += "'%s'," % str(stat) 
			#		else:
			#			update_sql += "%s," % str(stat)
			#	update_sql = update_sql[:-1] + "where week = %s and player_id = %s" %(week, self.ID)
			#	db_execute(update_sql)
				
			# If not, run insert
			#else:
			#	for stat in gamelog[row]:
					# Check if state needs to be input as string
			#		if isinstance(stat, basestring):
			#			stat = str(stat).translate(None, "',_")
			#			insert_sql += "'%s'," % str(stat)
			#		else:
			#			insert_sql += str(stat) + ','
			#	insert_sql = insert_sql[:-1] + ')'
			#	db_execute(insert_sql)								
		
	# Maps html stat name with db column name
	# Input: html stat column as string
	# Returns: db column as string
	def get_corres_col_name(self, stat):
		stat_dict = {
					'date': 'game_date',
					'opp': 'opp',
					'result': 'result',
					'victory': 'victory',
					'completions': 'completions',
					'pass attempts': 'pass_att',
					'passing yards': 'pass_yards',
					'completion percentage': 'compl_pct',
					'longest pass play': 'pass_long',
					'passing touchdowns': 'pass_td',
					'interceptions thrown': 'int_thrown',
					'passer (qb) rating': 'pass_rate',
					'raw total quarterback rating': 'raw_qbr',
					'adjusted total quarterback rating': 'adj_qbr',
					'rushing attempts': 'rush_att',
					'total rushing yards': 'rush_yards',
					'average yards per carry': 'rush_avg',
					'longest run': 'rush_long',
					'rushing touchdowns': 'rush_td',
					'total receptions': 'receptions',
					'total receiving yards': 'rec_yards',
					'receiving yards per game': 'rec_avg',
					'longest reception': 'rec_long',
					'receiving touchdowns': 'rec_td',
					'fgm 1-19 yards': 'fg_1_19',
					'fgm 20-29 yards': 'fg_20_29',
					'fgm 30-39 yards': 'fg_30_39',
					'fgm 40-49 yards': 'fg_40_49',
					'fgm 50+ yards': 'fg_50_plus',
					'field goals made': 'fg_made',
					'percentage of field goals made': 'fg_pct',
					'longest fgm': 'fg_long',
					'extra points made': 'xp_made',
					'extra points attempted': 'xp_att',
					'total kicking points': 'kick_points', 
					'total tackles': 'def_tot_tack',
					'unassisted tackles': 'def_unassist_tack',
					'assisted tackles': 'def_assist_tack',
					'sacks': 'def_sacks',
					'forced fumbles': 'def_force_fmble',
					'intercepted returned yards': 'def_int_ret_yrds',
					'avg': 'def_int_ret_avg',
					'longest interception return': 'def_int_ret_long',
					'interceptions returned for touchdowns': 'def_int_ret_td',
					'pass defended': 'def_pass_defend',
					'total punts': 'punt_total',
					'gross punting average': 'punt_avg',
					'longest punt': 'punt_long',
					'gross punting yards': 'punt_total_yrds'
					}
			
		return stat_dict[stat]
		
	# retrieve game log...needs work
	def get_stats(self):
		return null
	
	# retrieve individual stat
	# Input: stat_cat as string, table_name as string, date as string
	# Return: stat as float
	def get_statistic(self, stat_cat, table_name, date):
		
		
		select_sql = """
				select %s 
				from %s
				where game_date = '%s'
				and player_id = %s
				""" % (stat_cat, table_name, date, self.ID)
		
		result = float(db_execute(select_sql))
				
		return result
			
	# create player's stats table
	# Input: player table name
	# Returns:
	def create_player_stats_table(self, name):
		
		create_string = """create table %s (
			week int not null,
			player_id int not null,
			game_date varchar(10),
			player_name varchar(30),
			opp varchar(30),
			result varchar(20),
			victory varchar(1),
			completions int not null default 0,
			pass_att int not null default 0,
			pass_yards int not null default 0,
			compl_pct float not null default 0,
			pass_long int not null default 0,
			pass_td int not null default 0,
			int_thrown int not null default 0,
			pass_rate float not null default 0,
			raw_qbr float not null default 0,
			adj_qbr float not null default 0,
			rush_att int not null default 0,
			rush_yards int not null default 0,
			rush_avg float not null default 0,
			rush_long int not null default 0,
			rush_td int not null default 0,
			receptions int not null default 0,
			rec_yards int not null default 0,
			rec_avg float not null default 0,
			rec_long int not null default 0,
			rec_td int not null default 0,
			fg_1_19 int not null default 0,
			fg_20_29 int not null default 0,
			fg_30_39 int not null default 0,
			fg_40_49 int not null default 0,
			fg_50_plus int not null default 0,
			fg_made int not null default 0,
			fg_pct float not null default 0,
			fg_long int not null default 0,
			xp_made int not null default 0,
			xp_att int not null default 0,
			kick_points int not null default 0,
			def_tot_tack int not null default 0,
			def_unassist_tack int not null default 0,
			def_assist_tack int not null default 0,
			def_sacks float not null default 0,
			def_force_fmble int not null default 0,
			def_int_ret_yrds int not null default 0,
			def_int_ret_avg int not null default 0,
			def_int_ret_long int not null default 0,
			def_int_ret_td int not null default 0,
			def_pass_defend int not null default 0,
			punt_total int not null default 0,
			punt_avg float not null default 0,
			punt_long int not null default 0,
			punt_total_yrds int not null default 0,
			primary key (week, player_id)
			)""" % name
		
		db_execute(create_string)
		
	def getWeek(self, date):
		(month, day, year) = date.split('/')
		date = datetime(int(year), int(month), int(day))

		if date <= datetime(2016, 9, 5):
			return 1
		elif date <= datetime(2016, 9, 12):
			return 2
		elif date <= datetime(2016, 9, 19):
			return 3
		elif date <= datetime(2016, 9, 26):
			return 4
		elif date <= datetime(2016, 10, 3):
			return 5
		elif date <= datetime(2016, 10, 10):
			return 6
		elif date <= datetime(2016, 10, 17):
			return 7
		elif date <= datetime(2016, 10, 24):
			return 8
		elif date <= datetime(2016, 10, 31):
			return 9
		elif date <= datetime(2016, 11, 7):
			return 10
		elif date <= datetime(2016, 11, 14):
			return 11
		elif date <= datetime(2016, 11, 21):
			return 12
		elif date <= datetime(2016, 11, 28):
			return 13
		elif date <= datetime(2016, 12, 5):
			return 14
		return 0

				
	
	