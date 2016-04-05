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

#print_game_log(get_player_stats("http://espn.go.com/college-football/player/_/id/530541/brenden-motley"))
print datetime.datetime.now().time()
#print 'Retrieving rosters...'
[power_five_roster_links, power_five_team_names] = get_power_five_roster_links('http://espn.go.com/college-football/teams')
#update_stats(power_five_roster_links)

	
schedule = Schedule("Virginia Tech", "http://espn.go.com/college-football/team/schedule/_/id/259/virginia-tech-hokies")
schedule.get_schedule(schedule.url)
"""
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
"""
# test player class and db interface
#test_player = Player("John Lamb", 2, 'www.themanualoverride.com')
#print_game_log(get_player_stats("http://espn.go.com/college-football/player/_/id/511180/alex-howell"))
#Fitz = Player('Alex Howell', 511180, "http://espn.go.com/college-football/player/_/id/511180/alex-howell")
#Fitz.set_stats(get_player_stats("http://espn.go.com/college-football/player/_/id/511180/alex-howell"))
				
print datetime.datetime.now().time()

#print " ".join(power_five_roster_links[0].rsplit("/",1)[1].split("-"))




