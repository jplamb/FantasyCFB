#################################################
#  College Fantasy Football main program
#  Version 0.1
#  Created by John Lamb 
#  www.themanualoverride.com
#################################################

from getPlayers import get_power_five_roster_links, get_team_roster, print_players
from updateStats import update_stats
from Schedule import *
from getPlayerStats import get_player_stats
import Player
import datetime
from dbConn import db_execute, close_db, db_commit, open_db_connection
from teams import record_team
import Roster
from calcPoints import calc_all_player_points, calc_team_def_points, post_team_points

# Run console 
# inputs actions as list of choices (strs)
# returns selected action as int
def run_console(actions):
	print 'Welcome to the Fantasy Football League of Superb Champions II or FFLSCII'
	print 'Select an action from the list below:'
	
	while True:
		try:
			for count, act in enumerate(actions):
				print count + 1,
				print ')  ',
				print act

			print 'You only need to enter a number'
			print ''
			action  = int(raw_input('Enter an action\n'))
		except ValueError:
			print 'That\'s not a valid number, try again'
		else:
			print 'Executing now..'
			print datetime.datetime.now().time()
			break
		
	return action

# Use test data?
def run_test():
	test = ''
	while True:
		try:
			test = raw_input('Would you like to run in test mode? (y/n)').lower()
		except ValueError:
			print 'That\'s not a valid input, try again'
		except len(test) != 1:
			print 'That\'s not a valid input, try again'
		else:
			if test != 'y' and test != 'n':
				print 'Invalid value, try again'
				run_test()
			else:
				return test

# Initiate action
# inputs command as int
def perform_action(command):
	commands = {1 : 'con_get_players',
				2 : 'con_get_player_stats',
				3 : 'con_update_schedule',
				4 : 'con_print_schedule',
				5 : 'con_print_players',
				6 : 'con_update_rosters',
				7 : 'con_calculate_points'
				}
	
	possibles = globals().copy()
	possibles.update(locals())
	method = possibles.get(commands[command])
	if not method:
		raise NotImplementedError("Method %s does not exist" % commands[command])
	method()

# Get all rosters and all players on each team	
# returns list of name (str), id (int), url (str)
def con_get_players():
	[power_five_roster_links, power_five_team_names] = get_power_five_roster_links('http://espn.go.com/college-football/teams')
	

	#print power_five_roster_links
	players_list = [ [], [], [] ]
	for x in range(len(power_five_team_names)):
		name = power_five_team_names[x]
		roster_link = power_five_roster_links[x]
		team_id = roster_link.split('/')[-2]
		print name
		record_team(name, team_id)

		(urls, names, ids) = get_team_roster(roster_link, name)

		
	return players_list

# Get stats (game log) for players
# inputs names as list of string, id as list of ints, and url as list of strings
def con_get_player_stats():
	#(names, ids, urls) = con_get_players()
	#week = raw_input('What week is it?\n')

	game_logs = []
	
	sql = """
			select name, player_id, url
			from players
			"""
	result = db_execute(sql)
	#result = [['Jerod Evans', '556465','http://www.espn.com/college-football/player/_/id/556465/jerod-evans']]
	count = 1
	total = len(result)
	
	for player in result:
		name = player[0]
		id = player[1]
		url = player[2]
		print str(count) + ' / ' + str(total) + '  ' + name + '   ' + str(id)
		play_game_log = get_player_stats(url)
		
		if play_game_log:
			temp_player = Player.Player(name, id, url)
			temp_player.set_stats(play_game_log)
		if count % 25 == 0:
			pass
			#db_commit()
		count += 1
	#db_commit()
	"""
	for url in urls:
		#print url
		play_game_log = get_player_stats(url)
		#print play_game_log
		game_logs.append(play_game_log)
	
	con_save_player_stats(names, ids, urls,game_logs)
	"""

# Saves players stats to DB
# inputs names as list of strings, ids as list of ints, urls as list of strings, and game log as list
def con_save_player_stats(names, ids, urls, game_logs):
	for count,name in enumerate(names):
		temp_player = Player(name, ids[count], urls[count])
		temp_player.set_stats(game_logs[count])

# Get team schedules and update db
# inputs teams as list of strings and schedule_urls as list of strings
def con_update_schedule():
	[roster_urls, teams] = get_power_five_roster_links('http://espn.go.com/college-football/teams')
	
	
	for count,team in enumerate(teams):
		schedule_url = roster_urls[count].replace("roster", "schedule")
		temp_team = Schedule(team, schedule_url)
		temp_team.get_schedule(schedule_url)
		
		if count % 25 == 0:
			db_commit()
	db_commit()

# Outputs schedule as a text file
def con_print_schedule():
	no_team = Schedule(' ',' ')
	no_team.print_schedule()

# Outputs list of all players as a text file
def con_print_players():
	print_players();

# Get current rosters and store them in DB
def con_update_rosters():
	teams = ['Team John B', 'Team Jack', 'Team John L', 'Team Mike', 'Team Scott', 'Team Frankie']
	week = raw_input('What week is it?\n')
	
	for team in teams:
		temp_team = Roster.Roster(team)
		temp_team.update_roster(week)
	db_commit()

# Retrieve this weeks stats and save them to roster table
def con_post_team_stats():
	teams = ['Team John B', 'Team Jack', 'Team John L', 'Team Mike', 'Team Scott', 'Team Frankie']
	week = raw_input('What week is it?\n')
	
	for team in teams:
		temp_team = Roster.Roster(team)
		players = temp_team.team_players_bnch + temp_team.team_players_strt
		for player in players:
			pass
			#temp_player = Player()
			#temp_player.get_points()
			#temp_team.set_player_points(week, player)

def con_calculate_points():
	teams = ['Team_John_B', 'Team_Jack', 'Team_John_L', 'Team_Mike', 'Team_Scott', 'Team_Frankie']
	 
	week = int(raw_input('What week is it? \n'))
	
	calc_all_player_points(week)
	calc_team_def_points(week)
	
	post_team_points(week)
	
	
# Set test data
#test_player_link = "http://espn.go.com/college-football/player/_/id/530541/brenden-motley"
#test_get_roster_link = 'http://espn.go.com/college-football/teams'
#test_get_schedule = ['Virginia Tech', "http://espn.go.com/college-football/team/schedule/_/id/259/virginia-tech-hokies"]

# list of prompt options
action_choice = ['Retrieve players', 
				 'Get and store player data',
				 'Retrieve team schedule',
				 'Print schedule',
				 'Print players',
				 'Update Rosters',
				 'Calculate Points']
print datetime.datetime.now().time()

# run console
#test_mode = run_test()
open_db_connection(False)
command = run_console(action_choice)
perform_action(command)

close_db()
print 'Closing..'
print datetime.datetime.now().time()


# Legacy code
"""
[power_five_roster_links, power_five_team_names] = get_power_five_roster_links('http://espn.go.com/college-football/teams')
#update_stats(power_five_roster_links)

	
schedule = Schedule("Virginia Tech", "http://espn.go.com/college-football/team/schedule/_/id/259/virginia-tech-hokies")
schedule.get_schedule(schedule.url)

power_five_schedule_links = []
for count,link in enumerate(power_five_roster_links):
	power_five_schedule_links.append(link.replace("roster","schedule"))
	

filter(None,power_five_schedule_links)
for count,team in enumerate(power_five_team_names):
	#print team, " ", power_five_schedule_links[count]
	schedule = Schedule(team,power_five_schedule_links[count])
	#print schedule.url
	#print power_five_schedule_links[count]
	schedule.get_schedule(schedule.url)

# test player class and db interface
#test_player = Player("John Lamb", 2, 'www.themanualoverride.com')
#print_game_log(get_player_stats("http://espn.go.com/college-football/player/_/id/511180/alex-howell"))
#Fitz = Player('Alex Howell', 511180, "http://espn.go.com/college-football/player/_/id/511180/alex-howell")
#Fitz.set_stats(get_player_stats("http://espn.go.com/college-football/player/_/id/511180/alex-howell"))
				
print datetime.datetime.now().time()

#print " ".join(power_five_roster_links[0].rsplit("/",1)[1].split("-"))
"""



