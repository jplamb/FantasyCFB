##This program grabs player stats from an ESPN URL
##To do:
##    -Add findStats methods for each stat category
##    -Determine how to store data
##    -Determine how to crawl through every game in a week

from lxml import html
from bs4 import BeautifulSoup
import requests
import re
import datetime

# Get links to all power five conference teams' roster
# Input --> URL to teams page
# Output --> list of URLs
def get_power_five_roster_links(teamsURL):
	page = requests.get(teamsURL)
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.text, 'lxml')
	powerFive = ['ACC','SEC','Big Ten', 'Big 12','Pac-12']

	roster_links = []

	# Find div block containing power five conference, sort out non P5 conferences
	powerFiveTag = soup.find_all("h4", string=powerFive)
	for headerOne in powerFiveTag:
		# Jump up two levels to search block containing team names and URLs
		parentOne = headerOne.parent
		parentTwo = parentOne.parent
		parTwoDes = parentTwo.descendants
		for tag in parTwoDes:

			# Filter out links so only roster links remain
			if "espn.go.com" in unicode(tag):
				
				# Grab URL, remove html tags and text
				link = re.search("(?P<url>http://espn[^\s]+\")", unicode(tag)).group("url").rstrip('\"')
				link = link[:41] + "roster/" + link[41:]
				# Exclude duplicates
				if link not in roster_links:
					roster_links.append(link)
					
	return roster_links

# Retrieve team roster
def get_team_roster(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.content,'lxml')
	
	# Find all player tags
	players_soup = soup.find_all('a', href=re.compile("http://espn[^\s]+player+"))
	
	# Declare lists for player data
	players_name = []
	players_id = []
	players_url = []
	
	# For each player, grab their name, ID, and url
	for player in players_soup:
		players_name.append(player.string)
		players_id.append(re.search("id\/([^\s]+)\/",unicode(players_soup[0])).group(1))
		players_url.append(player['href'])
	
	# Pass back all three lists as one
	players = [players_name, players_id, players_url]
	return players

	
print datetime.datetime.now().time()
power_five_roster_links = get_power_five_roster_links('http://espn.go.com/college-football/teams')
for team in power_five_roster_links:
	player_list = get_team_roster(team)
print datetime.datetime.now().time()
#print " ".join(power_five_roster_links[0].rsplit("/",1)[1].split("-"))
#print player_list[0][0]
#print player_list[1][0]
#print player_list[2][0]
	
	





