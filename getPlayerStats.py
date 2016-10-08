########################################################
#  Retrieve player game log (stats)
#  Cleanse game log and prep for storage
#  3/13/16  John Lamb
########################################################

from lxml import html
from bs4 import BeautifulSoup, Tag
from unidecode import unidecode
import datetime
import requests
import re

# Stats grid header string
game_log_title = '2016 Game Log'

# Get gamelog for player
# Inputs: URL string to player's stat page
# Returns: game log as list of lists
def get_player_stats(url):
	try:
		page = requests.get(url)
	except Exception as e:
		logPlayerException(url)
		
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.content, 'lxml')
	
	# Get the grid containing game log...asssumes this is the second grid on the page
	#grids = soup.find_all("tr", attrs={"class": "stathead"})[1]
	#grids = soup.find_all("tr", attrs={"class": "stathead"})
	
	# Find game log grid from tags that match above criteria
	#stathead = []
	
	# Find player game stats grid
	game_log = soup.find(text=game_log_title)
	
	# If exists, assign appropriate tag as actual grid
	if game_log:
		stats_grid = game_log.parent.parent.parent
	
	# if no grid is found, log error
	if not game_log or not stats_grid:
		print 'no stats'
		return
		
	stats_grid_soup = BeautifulSoup(str(stats_grid), 'lxml')
	
	# remove @ symbols from grid so all rows are equal in length
	stat_rows_at = stats_grid_soup.find_all( text='@')
	
	for at in stat_rows_at:
		fixed = unicode(at).replace('@', '')
		at.replace_with(fixed)
	
	# find all rows in grid
	stat_rows = stats_grid_soup.find_all('tr')
	
	stats = {} # game log stats
	# make sure at least one game has been played and second row is column headers
	if len(stat_rows) > 2 and 'colhead' in stat_rows[1]['class']:
		row = stat_rows[1]
		
		# get headers..data, opp, and result have no class tag
		catsInfo = [x.string.lower().strip() for x in row.find_all('td', attrs = {'class': None})]
		catsStats = [str(x['title']).lower().strip() for x in row.find_all('td', {'title': True})]
		catsInfo.insert(2,'victory') # explicitly declare victory as a header
		count = 0
		
		for cat in catsInfo + catsStats:
			# grab all stats in each row and assign it to the corresponding category/header
			values = [x.get_text('\n', strip=True).split('\n')[count] for x in stat_rows[2:] if len(x.get_text('\n').split('\n')) > 1 and 'statistics' not in str(x)]

			# values is a list of each game's stats for the current category
			if cat in catsInfo:
				if cat == 'date':
					stats[cat] = [str(x) + "/" + str(datetime.datetime.now().year) for x in values]
				elif cat == 'opp':
					stats[cat] = [unidecode(x) for x in values]
				else:
					stats[cat] = values
			else:
				stats[cat] = values
			count += 1
			print cat, stats[cat]
	
	return stats

	for grid in grids:
		#for child in grid.children:
			if child.string and "2016 Game Log" in child.string:
				stathead = grid
				break
				
	# Exit if no game log is found
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
		# If row has data, add
		if len(row_data) > 0:
			game_log.append(row_data)
	return cleanse_game_log(game_log)

# Add zero values to prepr for database storage
# Inputs: game log as list of lists
# Returns: game log as list of lists
def cleanse_game_log(log):
	
	# Remove None types from log
	for row in log:
		if row == "":
			log.remove(row)
		for stat in row:
			if stat == "":
				row.remove(stat)
	
	# Remove informational rows like bowl game headers
	for row in log:
		if len(row) <= 1:
			log.remove(row)
	
	# Count number of columns in header row
	num_of_cols = 0
	for col in log[0]:
		num_of_cols += 1

	# Set all values to 0 if player has no data for that week
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
				#log[row][stat] = float(log[row][stat].replace("/", ""))
				log[row][stat] = str(log[row][stat])
			# Remove dashes in stat and set to zero
			elif "-" in str(log[row][stat]):
				log[row][stat] = 0.0
			else:
				log[row][stat] = float(log[row][stat])

	# Remove non ascii character
	for row in range(1,len(log)):
		for stat in range(0,2):
			log[row][stat] = ''.join((c for c in log[row][stat] if 0 < ord(c) < 128))
	
	# Add year to game date
	for row in range(1,len(log)):
		log[row][0] += "/" + str(datetime.datetime.now().year)
	
	return log
	
# Print game log
# Inputs: game log
# Returns
def print_game_log(log):
	for row in log:
		for stat in row:
			print stat,
		print "\n"

def logPlayerException(url):
	filename = 'playerStatsError.txt'
	f = open(filename,'a')
	f.write('\n')
    #if os.path.isfile(filename) and os.path.getsize(filename) == 0:
    #    f.write('Week, Player ID, Total Points, Elig Points, Unelig Points, week, player id, Game Date, Player Name, Opponent, Result, Pass Compl, Pass Att, Pass Yards, Compl Pct, Pass Long, Pass TD, Int Thrown, Pass Rate, Raw QBR, Adj QBR, Rush Att, Rush Yards, Rush Avg, Rush Long, Rush TD, Rec Receptions, Rec Yards, Rec Avg, Rec Long, Rec TD, FG 1-19, FG 20-29, FG 30-39, FG 40-49, FG 50+, FG Made, FG Pct, FG Long, XP Made, XP Att, Kick Points, Def Tackles, Def Unassist Tackles, Def Ass Tackles, Def Sacks, Def Forced Fumbles, Def Int Ret Yards, Def Int Ret Avg, Def Int Ret Long, Def Int Ret TD, Def Pass Defend, Punt Total, Punt Avg, Punt Total, Punt Total Yards')
	f.write('%s, '%(url))
	f.close()
		
