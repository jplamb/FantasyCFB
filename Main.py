##This program grabs player stats from an ESPN URL
##To do:
##    -Add findStats methods for each stat category
##    -Determine how to store data
##    -Determine how to crawl through every game in a week

from lxml import html
from bs4 import BeautifulSoup
import requests
import re

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
				
				# Exclude duplicates
				if link not in roster_links:
					roster_links.append(link)
					
	return roster_links
		
power_five_roster_links = get_power_five_roster_links('http://espn.go.com/college-football/teams')
for link in power_five_roster_links:
	print link
print len(power_five_roster_links)
	
	
	
	





