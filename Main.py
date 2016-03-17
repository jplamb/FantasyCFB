##This program grabs player stats from an ESPN URL
##To do:
##    -Add findStats methods for each stat category
##    -Determine how to store data
##    -Determine how to crawl through every game in a week

from lxml import html
from bs4 import BeautifulSoup, Tag
from getPlayers import get_power_five_roster_links, get_team_roster
from getPlayerStats import *
from Player import *
import requests
import re
import datetime
import MySQLdb
import base64


#print_game_log(get_player_stats("http://espn.go.com/college-football/player/_/id/530541/brenden-motley"))
print datetime.datetime.now().time()
print 'Retrieving rosters...'
#power_five_roster_links = get_power_five_roster_links('http://espn.go.com/college-football/teams')

# test player class and db interface
#test_player = Player("John Lamb", 2, 'www.themanualoverride.com')

Fitz = Player('Alex Howell', 511180, "http://espn.go.com/college-football/player/_/id/511180/alex-howell")
Fitz.set_stats(get_player_stats("http://espn.go.com/college-football/player/_/id/511180/alex-howell"))
				
"""
error_log = open('error_log.txt', 'w')
for team in power_five_roster_links:
	player_list=[[],[],[]]
	player_list.append(get_team_roster(team))
	player_list = filter(None, player_list)

	for player_set in player_list:
		for player in player_set:
			name = player[0]
			name = re.sub('[.-]', '', name)
			
			print str(datetime.datetime.now().time()) + ': Creating player - ' + str(name)
			temp = Player(name,player[1], player[2])
			print str(datetime.datetime.now().time()) + ':  Getting stats...'
			
			try:
				log = get_player_stats(temp.url)
			except IndexError:
				log = []
				
				error_log.write('%s had no stats (%s) \n %s' % (name, player[2], IndexError))
				error_log.write('\n')
				
			if log != []:
				print datetime.datetime.now().time(),':  Saving stats...'
				temp.set_stats(log)
				print datetime.datetime.now().time(),':  Success'
			else:
				print datetime.datetime.now().time(),':  Fail'
				error_log.write('%s has no log \n' % name)
			
error_log.close()
"""

print datetime.datetime.now().time()

#print " ".join(power_five_roster_links[0].rsplit("/",1)[1].split("-"))




