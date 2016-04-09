#################################################
#  College Fantasy Football main program
#  Version 0.1
#  Created by John Lamb 
#  www.themanualoverride.com
#################################################

from getPlayers import get_power_five_roster_links, get_team_roster
from updateStats import update_stats
from Schedule import *
import datetime
from dbConn import db_execute

def run_console():
	print 'Welcome to the Fantasy Football League of Superb Champions II or FFLSCII'
	print 'Select an action from the list below:'
	
	while True:
		try:
			for count, act in enumerate(actions):
				print count,
				print ')  ',
				print act

			print 'Enter a number'

			action  = int(raw_input('Enter an action'))
		except ValueError:
			print 'That\'s not a valid number, try again'
		else:
			print 'Executing now..'
			print datetime.datetime.now().time()
			break
		
	return action

def run_test():
	while True:
		try:
			test = char(raw_input('Would you like to run in test mode? (y/n)').lower())
		except ValueError:
			print 'That\'s not a valid input, try again'
		else:
			if test != 'y' and test != 'n':
				print 'Invalid value, try again'
				run_test()
			else:
				return test
			
def perform_action(command):
	commands = {1 : 'get_player_roster'
				}
				
def con_get_players():
	[power_five_roster_links, power_five_team_names] = get_power_five_roster_links('http://espn.go.com/college-football/teams')
	
	players_list = [ [], [], [] ]
	for team_url in power_five_roster_links:
		# [name, id, url]
		players_returned = get_team_roster(team_url)
		
		players_list[0].append(players_returned[0])
		players_list[1].append(players_returned[1])
		players_list[2].append(players_returned[2])
		
	return players_list

def con_get_player_stats(urls):
	
	game_logs = []
	
	for url in urls:
		play_game_log = get_player_stats(url)
		game_logs.append(play_game_log)
	
	return game_logs

def save_player_stats(names, ids, urls, game_logs):
	for count,name in enumerate(names):
		temp_player = Player(name, ids[count], urls[count])
		temp_player.set_stats(game_logs[count])
		
def con_update_schedule(teams, schedule_urls):
	
	for count,team in enumerate(teams):
		temp_team = Schedule(team, team_urls[count])
		temp_team.get_schedule(team_urls[count])
	

# Set test data
test_player_link = "http://espn.go.com/college-football/player/_/id/530541/brenden-motley"
test_get_roster_link = 'http://espn.go.com/college-football/teams'
test_get_schedule = ['Virginia Tech', "http://espn.go.com/college-football/team/schedule/_/id/259/virginia-tech-hokies"]

action_choice = ['Retrieve players', 
				 'Store player data'
				 'Retrieve team schedule]
print datetime.datetime.now().time()

test_mode = run_test()
command = run_console()
perform_action(command)


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



