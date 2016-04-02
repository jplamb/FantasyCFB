#############################################
# Retrieve schedule for all power five teams
# Created by John Lamb
#############################################

from dbConn import *
from lxml import html
from bs4 import BeautifulSoup
import requests
import re

class Schedule:
	
	# init stores teams and creates table
	# inputs: power_five_teams as list, schedule_urls as list of strings
	def __init__(self, power_five_team, schedule_url):
		self.team = power_five_team
		self.url = schedule_url
		
		if not check_table_exists("schedule"):
			self.create_table("schedule")
	

	# Crete table
	# inputs: table_name as string
	def create_table(self, table_name):
		
		open_db_connection()
		
		create_sql = """
				create table %s (
				team varchar(20) not null,
				week_1_opp varchar(20),
				week_1_time date,
				week_2_opp varchar(20),
				week_2_time date,
				week_3_opp varchar(20),
				week_3_time date,
				week_4_opp varchar(20),
				week_4_time date,
				week_5_opp varchar(20),
				week_5_time date,
				week_6_opp varchar(20),
				week_6_time date,
				week_7_opp varchar(20),
				week_7_time date,
				week_8_opp varchar(20),
				week_8_time date,
				week_9_opp varchar(20),
				week_9_time date,
				week_10_opp varchar(20),
				week_10_time date,
				week_11_opp varchar(20),
				week_11_time date,
				week_12_opp varchar(20),
				week_12_time date,
				week_13_opp varchar(20),
				week_13_time date,
				primary key (team) 
				)""" % table_name
		
		execute_sql(create_sql)
				
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
	def get_schedule(self, roster):
		
		date = []
		time = []
		opponent = []
		opp_id = []
		status = []
		
		# Loop through all rosters in list

		#for roster in roster_urls:
		page = requests.get(roster)
		tree = html.fromstring(page.content)
		soup = BeautifulSoup(page.text, 'lxml')

		# Get schedule block
		schedule_block = soup.find(id="showschedule")
		
		# Find rows of schedule table
		for tag in schedule_block.descendants:
			#print type(tag)
			#print tag
			
			# iterate through all schedule block tags
			try:
				if tag.has_attr('class') and tag is not None:
					# get game home/away status
					if 'game-status' in tag['class']:
						#print tag.string,
						if tag.string == 'vs':
							status.append('home')
						else:
							status.append('away')
					# get opponent
					elif 'team-name' in tag['class']:
						#print tag.string
						opponent.append(tag.string)
						opp_id_raw = tag.contents[0]['href']
						opp_id.append(opp_id_raw.split('/')[-2])
					# get game date and game time
					elif 'evenrow' in tag['class'] or 'oddrow' in tag['class']:
						#date
						#print tag.contents[0].string,
						date.append(tag.contents[0].string)
						#time
						#print tag.contents[2].string
						time.append(tag.contents[2].string)
			# handle tags without class attribute
			except AttributeError:
				pass
		
		for count, game in enumerate(opponent):
			print date[count],
			print " at ",
			print time[count]
			print status[count],
			print opponent[count],
			print "(", opp_id[count], ")"
			print ""
			
		
	# Insert schedule into table
	# inputs: date as list of strings, opp as list of strings
	def insert_schedule(self, date, opp):
		print ""		

		
		
		
		
		
		
		
		
		