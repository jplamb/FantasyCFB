########################################################
#  Retrieve player game log (stats)
#  Cleanse game log and prep for storage
#  3/13/16  John Lamb
########################################################

from lxml import html
from bs4 import BeautifulSoup, Tag
from time import strptime
import datetime
import requests
import re


def get_player_stats(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.content, 'lxml')
	
	# Get the grid containing game log...asssumes this is the second grid on the page
	#grids = soup.find_all("tr", attrs={"class": "stathead"})[1]
	grids = soup.find_all("tr", attrs={"class": "stathead"})
	
	stathead = []
	for grid in grids:
		for child in grid.children:
			if "Game Log" in child.string:
				stathead = grid
				break
	if stathead == []:
		return stathead
	# Grid header contains information about what stats follow (is player a QB, WR, RB, etc.)
	stat_catgs = [[]]
	for stat_catg in stathead.children:
		# Header also says how many stats are in each category
		if stat_catg.string != None and stat_catg != "":
			stat_catgs.append([stat_catg.string.lower(), stat_catg['colspan']])
	# Not sure what's going on here but list adds a null item at the beginning of the list
	stat_catgs.pop(0)
	
	
	game_log = [[]]
	# Walks through the game log table by row
	for sibling in stathead.next_siblings:
		row_data = []
						
		# Skip navigable strings...only interested in tags
		if sibling.__class__ == Tag and sibling is not None:
			
			# Check if header row and grab title attribute text
			if sibling['class'][0] == 'colhead':
				
				for child in sibling.children:
					
					# first few tags don't contain attributes...grab tag string instead
					if child.__class__ == Tag and not child.has_attr('title'):
						row_data.append(child.string.strip())
					elif child.string is not None and child.string != "" and child.__class__ == Tag:
						row_data.append(str(child['title']))
			else:
				# Steps through each stat in the row
				for child in sibling.children:
				
					# Standard row
					if child.string is not None and child.string != "":
						row_data.append(child.string.strip())
					# If row is an away game and grabs result
					else:
						for tag in child:
							if tag.string is not None and tag.name == 'a' and tag.string != "":
								row_data.append(tag.string)
	
					
		if len(row_data) > 0:
			game_log.append(row_data)
		
	return cleanse_game_log(game_log)

# Add zero values to prepr for database storage
def cleanse_game_log(log):
	
	# Remove None types from log
	for row in log:
		if row == "":
			log.remove(row)
		for stat in row:
			if stat == "":
				row.remove(stat)
	
	# Remove header rows like bowl game headers
	for row in log:
		if len(row) <= 1:
			log.remove(row)
	
	# Count number of columns in header row
	num_of_cols = 0
	for col in log[0]:
		num_of_cols += 1

	# Set all values to 0 if player was benched that week
	for row in log:
		if len(row) < num_of_cols and len(row) > 1:
			# Override 'No stats available string'
			row[3] = 0
			for stat in range(4, num_of_cols):
				row.append(0)
				
	# Convert all stats to floats
	for row in range(1,len(log)):
		for stat in range(3, num_of_cols):
			
			# Check if stat contains slash, indicates player is a kicker
			if "/" in str(log[row][stat]):
				log[row][stat] = float(log[row][stat].replace("/", ""))
			elif "-" in str(log[row][stat]):
				log[row][stat] = 0.0
			else:
				log[row][stat] = float(log[row][stat])
	
	# Remove non ascii character
	for row in range(1,len(log)):
		for stat in range(0,3):
			log[row][stat] = ''.join((c for c in log[row][stat] if 0 < ord(c) < 128))
	
	for row in range(1,len(log)):
		#log[row][0] = strptime(log[row][0], "%m/%d")  
		log[row][0] += "/" + str(datetime.datetime.now().year)

	return log
	
# Print game log
def print_game_log(log):
	for row in log:
		for stat in row:
			print stat,
		print "\n"