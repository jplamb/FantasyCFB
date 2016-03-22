#############################################
# Retrieve schedule for all power five teams
# Created by John Lamb
#############################################

from dbConn import *
from lxml import html
from bs4 import BeautifulSoup

class Schedule:
	
	# init stores teams and creates table
	# inputs: power_five_teams as list
	def __init__(self, power_five_teams):
		self.teams = power_five_teams
		
		if not check_table_exists("schedule"):
			create_table("schedule")
	
	# Crete table
	# inputs: table_name as string
	def create_table(self, table_name):
		
		open_db_connection()
		
		create_sql = """
				create table %s
				team varchar(20) not null
				week_1_opp varchar(20)
				week_1_time date
				week_2_opp varchar(20)
				week_2_time date
				week_3_opp varchar(20)
				week_3_time date
				week_4_opp varchar(20)
				week_4_time date
				week_5_opp varchar(20)
				week_5_time date
				week_6_opp varchar(20)
				week_6_time date
				week_7_opp varchar(20)
				week_7_time date
				week_8_opp varchar(20)
				week_8_time date
				week_9_opp varchar(20)
				week_9_time date
				week_10_opp varchar(20)
				week_10_time date
				week_11_opp varchar(20)
				week_11_time date
				week_12_opp varchar(20)
				week_12_time date
				week_13_opp varchar(20)
				week_13_time date
				primary key (team)
				""" % table_name
		
		cursor.execute(create_sql)
		
		self.get_schedule()
		
		close_db()
	
	# Get weekly opponent
	# inputs: team as string, week as date?
	def get_opponent(self, team, week):
		print ""
	
	# Get game time
	# inputs: team as string, week as date?
	def get_game_time(self, team, week):
		print ""
	
	# Retrieve the schedule and insert into db
	# inputs: roster_urls as list of strings
	def get_schedule(self, roster_urls):
		
		date = []
		team = []
		
		# Loop through all rosters in list
		for roster in roster_urls:
			page = requests.get(roster)
			tree = html.fromstring(page.content)
			soup = BeautifulSoup(page.text, 'lxml')
			
			# Get schedule block
			schedule_block = soup.find(id="showschedule")
			
			# Find rows of schedule table
			for tag in schedule_block.descendants:
				table_row = re.search("(odd|even)row team", unicode(tag))
				# set date
				date.append(table_row.child.string)
				
				# find opponent
				for child in tag.descendants:
					if child['class'] == 'team-name':
						team.append(child.string)
		
	# Insert schedule into table
	# inputs: date as list of strings, opp as list of strings
	def insert_schedule(self, date, opp):
		print ""		

		
		
		
		
		
		
		
		
		