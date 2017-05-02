from getPlayers import get_power_five_roster_links, get_team_roster
from getPlayerStats import *
from Player import *
import re
import datetime

# Retrieve all team links and create Player class for each player to save game log
def update_stats(team_links):

	# Log to record all failed player saves
	error_log = open('error_log.txt', 'w')
	
	# Loop through every team
	for team in team_links:
		
		# Store roster details (name, ID, url)
		player_list=[[],[],[]]
		player_list.append(get_team_roster(team))
		player_list = filter(None, player_list)
		
		# Loop through each team
		for player_set in player_list:
			# Loop through each player
			for player in player_set:
				
				# Get name and remove special characters for db compatibility
				name = player[0]
				name = re.sub("[-.']", "", name)
				
				# Create temporary player class to save data
				print str(datetime.datetime.now().time()) + ': Creating player - ' + str(name)
				temp = Player(name,player[1], player[2])
				print str(datetime.datetime.now().time()) + ':  Getting stats...'

				try:
					# Retrieve player's game log
					log = get_player_stats(temp.url)
				
				# Catch error if player has no game log
				except IndexError:
					log = []

					error_log.write('%s had no stats (%s) \n %s' % (name, player[2], IndexError))
					error_log.write('\n')
				
				# Save player's game log to db
				if log != []:
					print datetime.datetime.now().time(),':  Saving stats...'
					temp.set_stats(log)
					print datetime.datetime.now().time(),':  Success'
				else:
					print datetime.datetime.now().time(),':  Fail'
					error_log.write('%s has no log \n' % name)

	error_log.close()