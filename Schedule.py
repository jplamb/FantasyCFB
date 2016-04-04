#############################################
# Retrieve schedule for all power five teams
# Created by John Lamb
#############################################

# to do
# --convert team ID to name either as sql table or dictionary (store as ID and convert on retrieval?)
# --mask db operations in own class
# --format time correctly for storage
# --add update statements

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
		
		create_sql = """
				create table %s (
				team varchar(20) not null,
				gm_date date not null,
				opp varchar(20) not null,
				gm_time time,
				status varchar(4),
				primary key(team, gm_date)
				)""" % table_name
		
		db_execute(create_sql)
					
	# Get weekly opponent
	# inputs: team as string, week as date?
	def get_opponent(self, team, week):
		pass 
	
	# Get game time
	# inputs: team as string, week as date?
	def get_game_time(self, team, week):
		pass
	
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
						if tag.string == 'vs':
							status.append('home')
						else:
							status.append('away')
					# get opponent
					elif 'team-name' in tag['class']:
						#print tag.string
						opponent.append(tag.contents[0].string)
						opp_id_raw = tag.contents[0]['href']
						opp_id.append(opp_id_raw.split('/')[-2])
					# get game date and game time
					elif 'evenrow' in tag['class'] or 'oddrow' in tag['class']:
						#date
						date.append(tag.contents[0].string)
						#time
						time.append(tag.contents[2].contents[0].strip())
			# handle tags without class attribute
			except AttributeError:
				pass
		
		# Format date for storage
		for count, dt in enumerate(date):
			dt = dt.split(',')[1].strip()
			month = dt[:3]
			day = dt[4:]
			seq = (month, day)
			date[count] = ' '.join(seq)
			
		"""
		for count, game in enumerate(opponent):
			
			print date[count],
			print " at ",
			print time[count]
			print status[count],
			print opponent[count],
			print "(", opp_id[count], ")"
			print ""
			"""
			self.insert_schedule(date[count], opponent[count], status[count], time[count])
			
		
	# Insert schedule into table
	# inputs: date as formatted string, opp as string, status as string, and time as string
	def insert_schedule(self, date, opp, status, time):
		
		# check if time is TBD or not
		if time == 'TBD':
			insert_sql = """
				insert into schedule (
				team,
				gm_date,
				opp,
				status
				)
				values (
				'%s',
				str_to_date('%s', '%%b %%d' ),
				'%s',
				'%s'
				)
				""" %(self.team, date, opp, status)
		else:
			insert_sql = """
				insert into schedule (
				team,
				gm_date,
				opp,
				gm_time,
				status
				)
				values (
				'%s',
				str_to_date('%s', '%%b %%d' ),
				'%s',
				'%s',
				'%s'
				)
				""" %(self.team, date, opp, time, status)

		db_execute(insert_sql)
				
				
				
		
		

		
		
		
		
		
		
		
		
		