##This program grabs player stats from an ESPN URL
##To do:
##    -Add findStats methods for each stat category
##    -Determine how to store data
##    -Determine how to crawl through every game in a week

from lxml import html
from bs4 import BeautifulSoup, Tag
from getPlayers import get_power_five_roster_links, get_team_roster
from getPlayerStats import get_player_stats, cleanse_game_log, print_game_log
import requests
import re
import datetime

get_player_stats("http://espn.go.com/college-football/player/_/id/530541/brenden-motley")
	
print datetime.datetime.now().time()
power_five_roster_links = get_power_five_roster_links('http://espn.go.com/college-football/teams')

player_names = []
player_id = []
player_url = []
player_attrs = [[],[],[]]

#for team in power_five_roster_links:
#	player_list = get_team_roster(team)
#	player_attrs.append(player_list)
#	player_names.append(player_list[0])
#	player_id.append(player_list[1])
#	player_url.append(player_list[2])
	
print datetime.datetime.now().time()

#print " ".join(power_five_roster_links[0].rsplit("/",1)[1].split("-"))

#count = 1
#for player in player_names:
#	for name in player:
#		print str(count) + " ",
#		print name
#		count += 1



