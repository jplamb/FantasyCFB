#####################################################
#  Player class handles data saving for each player
#  Interfaces with mysql db
#  Created by John Lamb
#####################################################

import MySQLdb
import base64
from dbConn import Mysql
from datetime import datetime

# Player class interfaces with database to retrieve and store data
class Player:
	
	#table_name = ""
	
	# init...creates player's stats table if none exists
	def __init__(self, name, ID, url):
		self.name = name
		self.ID = ID
		self.url = url
		
		self.table_name = "player_stats"
		
		# Create data table if it doesn't exist
		#conn = Mysql(host='localhost', user='appuser', password=base64.b64decode('YXBwdXNlcg=='), database='ffbdev')
		self.conn = Mysql()
		table_exists_where = "table_name = '%s'" %(self.table_name)
		table_exists = self.conn.call_store_procedure('check_table_exists', self.table_name)
		
		if not table_exists:
			self.conn.call_store_procedure('create_player_stats')
				
	# Insert or Update rows of gamelog into db
	# Input: player's gamelog
	# Returns: 
	def set_stats(self, stats):
		# Loop through each row in the gamelog 
		#for row in range(1,len(gamelog)):
		for game in range(len(stats['date'])):

			#week = gamelog[row][0]
			week = stats['date'][game]
			week = self.getWeek(week)
						
			# Execute row check
			row_check_where = "player_id = %s and week = %s limit 1" %(self.ID, week)
			row_check = self.conn.select('player_stats', row_check_where, "'x'")				
			
			# Set update/insert base sql strings
			if row_check:
				self.update_game_row(stats, week, game)
			else:
				self.insert_game_row(stats, week, game)
					
	def update_game_row(self, stats, week, game):
		#update_sql = """update %s set """ % self.table_name
		stats_c = {}
		for k in stats.keys():
			k_p = self.get_corres_col_name(k)
			stats_c[k_p] = stats[k][game]
		stats_c['player_name'] = self.name
		update_where = 'week = %s and player_id = %s' %(week, self.ID)
		self.conn.update('player_stats', where=update_where, **stats_c)
	
	def insert_game_row(self, stats, week, game):
		stats_c = {}
		for k in stats.keys():
			k_p = self.get_corres_col_name(k)
			stats_c[k_p] = stats[k][game]
		stats_c['player_id'] = self.ID
		stats_c['week'] = week
		stats_c['player_name'] = self.name
		self.conn.insert('player_stats', **stats_c)
		
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

				
	
	