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
	def set_stats(self):
		self.open_db_connection()
		
		self.check_table_exists()
		
		self.close_db()
	
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
			points int)""" % name

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