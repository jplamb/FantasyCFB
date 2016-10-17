#############################################
# Retrieve schedule for all power five teams
# Created by John Lamb
#############################################

# to do

from dbConn import Mysql
from lxml import html
from bs4 import BeautifulSoup
import requests
import re
from dateutil.parser import parse
from datetime import date, timedelta

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
				power_five varchar(1),
				win_loss varchar(3),
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
		win_loss_list = []
		
		# Loop through all rosters in list

		#for roster in roster_urls:
		page = requests.get(roster)
		tree = html.fromstring(page.content)
		soup = BeautifulSoup(page.text, 'lxml')

		# Get schedule block
		schedule_block = soup.find(id="showschedule")
		grid_rows_soup = BeautifulSoup(str(schedule_block), 'lxml')
		grid_rows = grid_rows_soup.find_all("tr")
		print self.team
		for row in grid_rows:
			if 'stathead' not in row['class'] and 'colhead' not in row['class'] :
				cur_date = row.td.string
				cur_date = parse(cur_date).date()
				date.append(cur_date)
				
				game_status = row.find(attrs={"class": "game-status"})
				if game_status.string == 'vs':
					status.append('home')
				else:
					status.append('away')

				opp_name = row.find(attrs={"class": "team-name"})
				opponent.append(opp_name.a.string.replace("'", ''))
				
				opp_id_raw = opp_name.a['href']
				opp_id.append(opp_id_raw.split('/')[-2])
				
				win_loss = row.find(attrs={"class": re.compile("win|loss")})

				if win_loss:
					if win_loss.string == 'W':
						win_loss = 'W'
					else:
						win_loss = 'L'
					time_raw = 'NA'
				else:
					win_loss = 'NA'
					time_raw = row.find_all('td')[2].contents[0].string
				win_loss_list.append(win_loss)

				time.append(time_raw)

		# Record schedule by row
		for count, game in enumerate(opponent):
			self.record_schedule(date[count], opponent[count], status[count], time[count], opp_id[count], win_loss_list[count])
	
	# Handle schedule updates
	# input date as string, opp as string, status as string, and time as string
	def record_schedule(self, date, opp, status, time, opp_id, victory):
		
		opp_power_five = self.is_power_five_team(opp_id)
		
		row_exists_sql = """
			select (1)
			from schedule
			where team = '%s'
			and gm_date = str_to_date('%s', '%%Y-%%m-%%d' )
			""" % (self.team, date)
		
		if db_execute(row_exists_sql):
			self.update_schedule(date, opp, status, time, opp_power_five, victory)
		else:
			self.insert_schedule(date, opp, status, time, opp_power_five, victory)
		
	# Insert schedule into table
	# inputs: date as formatted string, opp as string, status as string, and time as string
	def insert_schedule(self, date, opp, status, time, opp_power, victory):
		
		# check if time is TBD or not
		if time == 'TBD' or time == 'NA':
			insert_sql = """
				insert into schedule (
				team,
				gm_date,
				opp,
				status,
				power_five,
				win_loss
				)
				values (
				'%s',
				str_to_date('%s', '%%Y-%%m-%%d' ),
				'%s',
				'%s',
				'%s',
				'%s'
				)
				""" %(self.team, date, opp, status, opp_power, victory)
		else:
			insert_sql = """
				insert into schedule (
				team,
				gm_date,
				opp,
				gm_time,
				status,
				power_five,
				win_loss
				)
				values (
				'%s',
				str_to_date('%s', '%%Y-%%m-%%d' ),
				'%s',
				time_format('%s', '%%h:%%i %%p'),
				'%s',
				'%s',
				'%s'
				)
				""" %(self.team, date, opp, time, status, opp_power, victory)
		print insert_sql
		db_execute(insert_sql)
	
	# Update schedule row in table
	# inputs: date as formatted string, opp as string, status as string, and time as string
	def update_schedule(self, date, opp, status, time, opp_power, victory):
		
		if time == 'TBD' or time == 'NA':
			update_sql = """
				update schedule 
				set 
				opp = '%s',
				status = '%s',
				power_five = '%s',
				win_loss = '%s'
				where
				team = '%s' and
				gm_date = str_to_date('%s', '%%Y-%%m-%%d' )
				""" % (opp, status, opp_power, victory, self.team, date)
		else:
			update_sql = """
				update schedule 
				set 
				opp = '%s',
				gm_time = time_format('%s', '%%h:%%i %%p'),
				status = '%s',
				power_five = '%s',
				win_loss = '%s'
				where
				team = '%s' and
				gm_date = str_to_date('%s', '%%Y-%%m-%%d' )
				""" % (opp, time, status, opp_power, victory, self.team, date)		
		print update_sql
		db_execute(update_sql)
		
	# is team a power five team?
	# Input team_id as string
	# returns Y or N 
	def is_power_five_team(self, team_id):
		
		select_sql = """
				select (1)
				from teams
				where team_id = %s
				""" % (team_id)
		
		if db_execute(select_sql):
			return 'Y'
		else:
			return 'N'
	
	# Output schedule as text file
	def print_schedule(self):
		start_date = date(2016, 8, 30)
		end_date = date(2016, 12, 15)
		
		teams = self.get_power_five_teams()
		
		f = open('schedule2016.txt','w')
		f.write('Team, ')
		while start_date < end_date:
			week_end = start_date + timedelta(days=6)
			f.write(' %s - %s, '%(start_date.strftime('%m/%d'), week_end.strftime('%m/%d')))
			start_date = week_end + timedelta(days=1)

		for team in teams:
			team = team[0]
			
			start_date = date(2016, 8, 30)
			f.write('\n%s, ' %(team))
			while start_date < end_date:
				week_end = start_date + timedelta(days=6)

				sql = """
					select team, opp, power_five
					from schedule
					where team = '%s'
					and gm_date between str_to_date('%s', '%%Y-%%m-%%d' )
					and str_to_date('%s', '%%Y-%%m-%%d' )
					"""% (team, start_date, week_end)
				result = db_execute(sql)
				if result:
					print result[0]
					f.write(' %s, '%(result[0][1]))
				else:
					f.write(' No Game, ')
				start_date = week_end + timedelta(days=1)
		f.close()
		
	# Returns list of teams in the db which assumes only P5 teams are stored
	def get_power_five_teams(self):
		sql = """
			select team from teams
			"""
		teams = db_execute(sql)
		
		return teams
		
		
		
		
		