#####################################################
#  Player class handles data saving for each player
#  Interfaces with mysql db
#  Created by John Lamb
#####################################################

import MySQLdb
import base64

# Player class interfaces with database to retrieve and store data
class Player:
	
	#table_name = ""
	
	# init...creates player's stats table if none exists
	def __init__(self, name, ID, url):
		self.name = name
		self.ID = ID
		self.url = url
		
		self.table_name = "_".join(name.lower().split(" "))
		
		# Create data table if it doesn't exist
		if not self.check_table_exists(self.table_name):
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
	def set_stats(self, gamelog):
		
		# Make sure the table exists first
		if not self.check_table_exists(self.table_name):
			self.create_player_stats_table(self.table_name)			
		
		# Base string for insert statement
		insert_sql_cols = 'insert into %s (' % self.table_name

		# Generate insert statement base with columns
		for colname in gamelog[0]:
			insert_sql_cols += self.get_corres_col_name(str(colname).replace(" ","_").lower()) + ','
		insert_sql_cols = insert_sql_cols[:-1] + ') values ('
		
		self.open_db_connection()
		
		# Generate SQL insert/update statements for each row in gamelog
		# Loop through each row in the gamelog except header row
		for row in range(1,len(gamelog)):
			
			# SQL to check if row already exists in db
			row_check = """select count(1) 
						from %s 
						where game_date = '%s' """ 
			
			# Set update/insert base sql strings
			update_sql = """update %s set """ % self.table_name
			insert_sql = insert_sql_cols
			
			# Execute row check
			row_check = row_check % (self.table_name, gamelog[row][0])
			cursor.execute(row_check)
			
			# If already in db, run update
			if cursor.fetchone()[0]:
				for count, stat in enumerate(gamelog[row]):
					update_sql += self.get_corres_col_name(str(gamelog[0][count]).replace(" ","_").lower()) + '='
					
					# Make sure string type columns take in data as string format
					if isinstance(stat, basestring):
						update_sql += "'%s'," % str(stat) 
					else:
						update_sql += "%s," % str(stat)
				update_sql = update_sql[:-1] + "where game_date = '%s'" %gamelog[0][0]
				cursor.execute(update_sql)
				
			# If not, run insert
			else:
				for stat in gamelog[row]:
					# Check if state needs to be input as string
					if isinstance(stat, basestring):
						insert_sql += "'%s'," % str(stat)
					else:
						insert_sql += str(stat) + ','
				insert_sql = insert_sql[:-1] + ')'
				cursor.execute(insert_sql)
													
		self.close_db()
		
	# Maps html stat name with db column name
	# Input: html stat column as string
	# Returns: db column as string
	def get_corres_col_name(self, stat):
		stat_dict = {
					'date': 'game_date',
					'opp': 'opp',
					'result': 'result',
					'completions': 'completions',
					'pass_attempts': 'pass_att',
					'passing_yards': 'pass_yards',
					'completion_percentage': 'compl_pct',
					'longest_pass_play': 'pass_long',
					'passing_touchdowns': 'pass_td',
					'interceptions_thrown': 'int_thrown',
					'passer_(qb)_rating': 'pass_rate',
					'raw_total_quarterback_rating': 'raw_qbr',
					'adjusted_total_quarterback_rating': 'adj_qbr',
					'rushing_attempts': 'rush_att',
					'total_rushing_yards': 'rush_yards',
					'average_yards_per_carry': 'rush_avg',
					'longest_run': 'rush_long',
					'rushing_touchdowns': 'rush_td',
					'total_receptions': 'receptions',
					'total_receiving_yards': 'rec_yards',
					'receiving_yards_per_game': 'rec_avg',
					'longest_reception': 'rec_long',
					'receiving_touchdowns': 'rec_td',
					'fgm_1-19_yards': 'fg_1_19',
					'fgm_20-29_yards': 'fg_20_29',
					'fgm_30-39_yards': 'fg_30_39',
					'fgm_40-49_yards': 'fg_40_49',
					'fgm_50+_yards': 'fg_50_plus',
					'field_goals_made': 'fg_made',
					'percentage_of_field_goals_made': 'fg_pct',
					'longest_fgm': 'fg_long',
					'extra_points_made': 'xp_made',
					'extra_points_attempted': 'xp_att',
					'total_kicking_points': 'kick_points', 
					'total_tackles': 'def_tot_tack',
					'unassisted_tackles': 'def_unassist_tack',
					'assisted_tackles': 'def_assist_tack',
					'sacks': 'def_sacks',
					'forced_fumbles': 'def_force_fmble',
					'intercepted_returned_yards': 'def_int_ret_yrds',
					'avg': 'def_int_ret_avg',
					'longest_interception_return': 'def_int_ret_long',
					'interceptions_returned_for_touchdowns': 'def_int_ret_td',
					'pass_defended': 'def_pass_defend',
					'total_punts': 'punt_total',
					'gross_punting_average': 'punt_avg',
					'longest_punt': 'punt_long',
					'gross_punting_yards': 'punt_total_yrds'
					}
			
		return stat_dict[stat]
		
	# retrieve game log...needs work
	def get_stats(self):
		return null
	
	# retrieve individual stat
	def get_statistic(self, stat_cat):
		return null
	
	# create player's stats table
	# Input: player table name
	# Returns:
	def create_player_stats_table(self, name):
		self.open_db_connection()
		
		create_string = """create table %s (
			game_date varchar(10) not null,
			opp varchar(20),
			result varchar(20),
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
			primary key (game_date)
			)""" % name
		
		cursor.execute(create_string)
		
		self.close_db()
	
	# open db connection to ffbdev
	def open_db_connection(self):
		global db
		global cursor
		db = MySQLdb.connect('localhost', 'appuser', base64.b64decode('YXBwdXNlcg=='), 'ffbdev')
	
		cursor = db.cursor()
	
	# close db connection to ffbdev and commit
	def close_db(self):
		db.commit()
		db.close()
	
	# check if table exists
	# Inputs: player table name
	# Returns boolean if table exists
	def check_table_exists(self, name):
		self.open_db_connection()
		
		show = 'show tables like \'%s\'' % name
		result = cursor.execute(show)
		
		if result:
			self.close_db()
			return True
		
		self.close_db()
		return False