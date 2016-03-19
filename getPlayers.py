########################################################
#  Retrieve all power five conference teams' rosters
#  Retrieve all player names, IDs, and URLs
#  3/13/16  John Lamb
########################################################

from lxml import html
from bs4 import BeautifulSoup, Tag
import requests
import re

# Retrieve all power five conference teams' rosters
# Inputs: URL string to page with all college football teams' rosters
# Returns: string list of every teams' roster url
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
# Inputs: team url as string
# Returns: players' info as list of lists
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
	player_info = [[],[],[],[]]
	
	# For each player, grab their name, ID, and url
	for player in players_soup:
		if player is not None and player.string is not None:
			player_info.append([player.string, re.search("id\/([^\s]+)\/",unicode(players_soup[0])).group(1),player['href']])
		#players_name.append(player.string)
		#players_id.append(re.search("id\/([^\s]+)\/",unicode(players_soup[0])).group(1))
		#players_url.append(player['href'])
	
	# Pass back all three lists as one
	players = [players_name, players_id, players_url]
	
	# Filter out empty sets
	player_info = filter(None, player_info)
	player_info = [x for x in player_info if x!= None and x != []]
	
	return player_info

