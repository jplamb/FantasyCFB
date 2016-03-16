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
		
	# Insert or Update rows of gamelog into db
	def set_stats(self, gamelog):
		
		# Make sure the table exists first
		if not self.check_table_exists(self.table_name):
			self.create_player_stats_table(self.table_name)
		
		# SQL to check if row already exists in db
		row_check = """select count(1) 
						from %s 
						where game_date = '%s' """ 
			
		
		update_sql = """update %s set """ % self.table_name
		insert_sql = 'insert into %s (' % self.table_name
		
		# Generate insert statement columns
		for colname in gamelog[0]:
			insert_sql += self.get_corres_col_name(str(colname).replace(" ","_").lower())
		insert_sql += ') values ('
		
		self.open_db_connection()
		
		# Loop through each row in the gamelog except header row
		for row in range(1,len(gamelog)):
			
			# Check if row is in db
			row_check = row_check % (self.table_name, gamelog[row][0])
			cursor.execute(row_check)
			
			# If already in db, run update
			if cursor.fetchone()[0]:
				for count, stat in enumerate(row):
					update_sql += self.get_corres_col_name(str(gamelog[0][count]).replace(" ","_").lower()) + stat + ','
				update_sql = update_sql[:-1] + "where game_date = '%s'" %gamelog[0][0]
				print update_sql
				#cursor.execute(update_sql)
				
			# If not, run insert
			else:
				for stat in row:
					insert_sql += stat + ','
				insert_sql = insert_sql[:-1] + ')'
				print insert_sql
				#cursor.execute(insert_sql)
														
		self.close_db()
		
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
					'total_receiving yards': 'rec_yards',
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
					'total_kicking_points': 'kick_points' }
			
		return stat_dict[stat]
		
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