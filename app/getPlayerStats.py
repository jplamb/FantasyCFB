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
GAME_LOG_TITLE = '2016 Game Log'

# Get gamelog for player
# Inputs: URL string to player's stat page
# Returns: game log as list of lists
def get_player_stats(pageContent):

	soup = BeautifulSoup(pageContent, 'lxml')
	
	# Find player game stats grid
	game_log = soup.find(text=GAME_LOG_TITLE)
	
	# If exists, assign appropriate tag as actual grid
	if game_log:
		stats_grid = game_log.parent.parent.parent
	else:
		#print 'no stats'
		return
	
	# if no grid is found, log error
	if not stats_grid:
		#print 'no stats'
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
		#catsStats = [str(x['title']).lower().strip() for x in row.find_all('td', {'title': True})]
		catsStats = [str(x['title']).lower().strip() if x.has_attr('title') else str(x.text).lower() for x in row.find_all('td', {'class': True})]
		catsInfo.insert(2,'victory') # explicitly declare victory as a header
		count = 0
		
		for cat in catsInfo + catsStats:
			# grab all stats in each row and assign it to the corresponding category/header
			values = [x.get_text('\n', strip=True).split('\n')[count] for x in stat_rows[2:] if len(x.get_text('\n').split('\n')) > 1 and 'statistics' not in str(x) and 'postponed' not in str(x) and re.search("(PM|AM)", str(x)) == None]

			# values is a list of each game's stats for the current category
			if cat in catsInfo:
				if cat == 'date':
					stats[cat] = [str(x) + "/" + str(datetime.datetime.now().year) for x in values]
				elif cat == 'opp':
					stats[cat] = [unidecode(x) for x in values]
				elif cat == 'result':
					stats[cat] = [x if ' ' not in x else x.split(' ')[0] for x in values]
				else:
					stats[cat] = values
			else:
				stats[cat] = values
			count += 1
			#print cat, stats[cat]
	return stats

