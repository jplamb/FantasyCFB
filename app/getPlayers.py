########################################################
#  Retrieve all power five conference teams' rosters
#  Retrieve all player names, IDs, and URLs
#  3/13/16  John Lamb
########################################################

from lxml import html
from bs4 import BeautifulSoup, Tag
import requests
import re
from dbConn import Mysql

# Retrieve all power five conference teams' rosters
# Inputs: URL string to page with all college football teams' rosters
# Returns: string list of every teams' roster url
def get_power_five_roster_links(teamsURL):
	page = requests.get(teamsURL)
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.text, 'lxml')
	powerFive = ['ACC','SEC','Big Ten', 'Big 12','Pac-12', 'FBS Independents']

	roster_links = []
	team_names = []

	# Find div block containing power five conference, sort out non P5 conferences
	powerFiveTag = soup.find_all("h4", string=powerFive)
	for headerOne in powerFiveTag:
		# Jump up two levels to search block containing team names and URLs
		parentOne = headerOne.parent
		parentTwo = parentOne.parent
		testsoup = BeautifulSoup(str(parentTwo), 'lxml')
		teams = testsoup.find_all("h5")

		for team in teams:
			team_name = team.a.string

			if headerOne.string == 'FBS Independents':
				if team_name == 'BYU' or team_name == 'Notre Dame':
					pass
				else:
					continue

			link = team.a['href']
			ind = team.a['href'].find('team')
			if ind >= 0:
				link = link[:ind+5] + "roster/" + link[ind+5:]
			
			if team_name not in team_names and len(link) > 0:
				team_names.append(team_name)
				roster_links.append(link)

	return [roster_links, team_names]

# Retrieve team roster
# Inputs: team url as string
# Returns: players' info as list of lists
def get_team_roster(url, team_name):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	soup = BeautifulSoup(page.content,'lxml')
	
	# Find all player tags
	#players_soup = soup.find_all('a', href=re.compile("http://espn[^\s]+player+"))
	
	# Get Roster table
	player_grid = soup.find('div', {'id':'my-teams-table', 'class':'col-main'})
	# Find each player link tag
	grid_soup = BeautifulSoup(str(player_grid),'lxml')
	player_links = grid_soup.find_all('a')
	# Get stathead...may be useful in the future
	colhead = grid_soup.find('tr',{'class':'colhead'})
	statcat_soup = BeautifulSoup(str(colhead),'lxml')
	# But for now, use the length to exclude stat categories from player extraction
	statcats = statcat_soup.find_all('a')
	
	# Declare lists for player data
	players_name = []
	players_id = []
	players_url = []
	players_pos = []
	
	# Populate lists with each player
	for link in player_links[len(statcats):]:
		if link.has_attr('href'):
			players_url.append(link['href'])
			players_name.append(link.string)
			players_id.append(re.search("id\/([^\s]+)\/",link['href']).group(1))
			#print players_name[-1], players_id[-1], players_url[-1]
			pos = link.parent.next_sibling.string
			players_pos.append(pos)
				
	# Insert player into player table in DB
	for k in range(len(players_name)):	
		add_to_player_table(players_name[k],players_url[k], players_id[k], team_name, players_pos[k])
	
	return (players_url, players_name, players_id)

# Adds player to 'player' table
# inputs: player_info as array of player (str), ID (int), url (str) and team (str) 
def add_to_player_table(play_name, play_url, player_id, team, pos):
		
	# strip names of special characters
	name = re.sub("[-.']", "", play_name)
	#player_id = player_info[1]
	# escape apostrophes in url
	url = re.sub("[']", "''", play_url)
	
	values = {}
	values['name'] = name
	values['url'] = url
	values['team'] = team
	values['position'] = pos
	values['player_id'] = player_id
	
	conn = Mysql()
	
	# check if player already exists in db
	row_check_where = "player_id = %s"%(player_id)
	row_check = conn.select('players', row_check_where, "'x'")
	
	# run either update or insert if row exists or not
	if row_check:
		update_where = "player_id = %s"%(values['player_id'])
		values.pop('player_id', 0)
		conn.update('players', update_where, **values)
	else:
		conn.insert('players', **values)

# Output all players to text file			
def print_players():
		
		f = open('players2016.txt','w')
		f.write('Player, Team, Position')

		sql = """
				select name, team, position
				from players
				"""
				
		result = db_execute(sql)
		
		for player in result:
			f.write('\n%s, %s, %s'%(player[0], player[1], player[2]))
		f.close()