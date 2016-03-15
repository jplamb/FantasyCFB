# Outline for saving player data

# Table structure
#  table for each player
# Should table have columns unique to player position or contain all possible columns?
#  Original excel sheets was agnostic of player position

# So a player table should include the following columns:
#  Date  |  Opponent  |  Result  |  Completions  |  Pass Att  |  Pas  Yards  |  Completion %  |  Longest Pass Play
#  Passing TDs  |  Interceptions Thrown  |  Passer Rating  |  Raw QBR  |  Adj QBR
#  Rushing Att  |  Rush Yards  |  Rush Avg  |  Rush Long  |  Rush TD 
#  Receptions  |  Rec Yards  | Rec Avg  |  Rec long  |  Rec TD
#  FG 1-19  |  FG 20-29  |  FG 30-39  |  FG 40-49  |  FG 50+  |  FG Made  |  FG %  |  FG Long
#  Extra Points Made  |  XP Att  |  Points

import MySQLdb
import base64

# Player class interfaces with database to retrieve and store data
class Player:
	
	table_name = ""
	
	# init...creates player's stats table if none exists
	def __init__(self, name, ID, url):
		self.name = name
		self.ID = ID
		self.url = url
		
		table_name = "_".join(name.lower().split(" "))
		
		if not self.check_table_exists(table_name):
			self.create_player_stats_table(table_name)
		
	# set/save stats...needs work
	def set_stats(self, gamelog):
		self.open_db_connection()
		
		if not self.check_table_exists(table_name):
			self.create_player_stats_table(table_name)
		
		row_check = """select count(1) 
						from %s 
						where game_date = '%s' """ 
		
		update_sql = """update %s
					set 
					opp = %s,
					result = %s,
					completions = %i,
					pass_att = %i,
					pass_yards = %i,
					compl_pct = %f,
					pass_long = %i,
					pass_td = %i,
					int_thrown = %i,
					pass_rate = %f,
					raw_qbr = %f,
					adj_qbr = %f,
					rush_att = %i,
					rush_yards = %i,
					rush_avg = %f,
					rush_long = %i,
					rush_td = %i,
					receptions = %i,
					rec_yards = %i,
					rec_avg = %f,
					rec_long = %i,
					rec_td = %i,
					fg_1_19 = %i,
					fg_20_29 = %i,
					fg_30_39 = %i,
					fg_40_49 = %i,
					fg_50_plus = %i,
					fg_made = %i,
					fg_pct = %f,
					fg_long = %i,
					xp_made = %i,
					xp_att = %i,
					points = %i
					where game_date = %s"""
		for row in gamelog:
			row_check = row_check % (table_name, row[0])
			cursor.execute(row_check)
			
			if cursor.fetchone()[0]:
				update_sql = update_sql
																		
		
		self.close_db()
		
	def process_weekly_stats(self, header_row, gamelog_row):
		stat_dict = {
					'date': 1,
					'opp': 2,
					'result': 3,
					'completions': 4,
					'pass attempts' = 5,
					'passing yards' = 6,
					'completion percentage' = 7,
					'longest pass play' = 8,
					'passing touchdowns' = 9,
					'interceptions thrown' = 10,
					'passer (qb) rating' = 11,
					'raw total quaterback rating' = 12,
					'adjusted total quarterback rating' = 13,
					'rushing attempts' = 14,
					'total rushing yards' = 15,
					'average yards per carry'= 16,
					'longest run' = 17,
					'rushing touchdowns' = 18,
					'total receptions' = 19,
					'total receiving yards' = 20,
					'receiving yards per game' = 21,
					'longest reception' = 22,
					'receiving touchdowns' = 23,
					'fgm 1-19 yards' = 24,
					'fgm 20-29 yards' = 25,
					'fgm 30-39 yards' = 26,
					'fgm 40-49 yards' = 27,
					'fgm 50+ yards' = 28,
					'field goals made' = 29,
					'percentage of field goals made' = 30,
					'longest fgm' = 31,
					'extra points made' = 32,
					'extra points attempted' = 33,
					'total kicking points' = 34 )
		
	# retrieve game log...needs work
	def get_stats(self):
		return null
	
	# retrieve individual stat
	def get_statistic(self, stat_cat):
		return null
	
	# create player's stats table
	def create_player_stats_table(self, name):
		self.open_db_connection()
		
		create_string = """create table %s (
			game_date date not null,
			opp varchar(20),
			result varchar(20),
			completions int,
			pass_att int,
			pass_yards int,
			compl_pct float,
			pass_long int,
			pass_td int,
			int_thrown int,
			pass_rate float,
			raw_qbr float,
			adj_qbr float,
			rush_att int,
			rush_yards int,
			rush_avg float,
			rush_long int,
			rush_td int,
			receptions int,
			rec_yards int,
			rec_avg float,
			rec_long int,
			rec_td int,
			fg_1_19 int,
			fg_20_29 int,
			fg_30_39 int,
			fg_40_49 int,
			fg_50_plus int,
			fg_made int,
			fg_pct float,
			fg_long int,
			xp_made int,
			xp_att int,
			points int
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
	
	# close db connection to ffbdev
	def close_db(self):
		db.close()
	
	# check if table exists
	def check_table_exists(self, name):
		self.open_db_connection()
		
		show = 'show tables like \'%s\'' % name
		result = cursor.execute(show)
		
		if result:
			self.close_db()
			return True
		
		self.close_db()
		return False