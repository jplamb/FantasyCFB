##This program grabs player stats from an ESPN URL
##To do:
##    -Add findStats methods for each stat category
##    -Determine how to store data
##    -Determine how to crawl through every game in a week

from lxml import html
from bs4 import BeautifulSoup
import requests
import re

# Finds the tag with a plyaer name
def findPlayer(tag):
  return tag.has_attr('name') and tag.has_attr('href') and tag.name == 'a'

# Grabs stats for each type
def findPassingStats(tag):
    passingStat = ['\'c-att\'','yds','avg','td','int','qbr']
    return  'class' in tag.attrs and(tag['class'] == ['name'] or tag['class'] == ['yds'] or
                                     tag['class'] == ['c-att'] or tag['class'] == ['avg'] or
                                     tag['class'] == ['td'] or tag['class'] == ['int'] or
                                      tag['class'] == ['qbr'] )

# Finds all stat categories on page
def statCats(tag):
    return (tag.name == 'div' and tag.has_attr('id') and
            (tag['id'] == ['gamepackage-passing'] or tag['id'] == ['gamepackage-rushing'] or
            tag['id'] == ['gamepackage-receiving'] or tag['id'] == ['gamepackage-interceptions'] or
            tag['id'] == ['gamepackage-kickReturns'] or tag['id'] == ['gamepackage-kicking'] or
            tag['id'] == ['gamepackage-punting']))

# Get page URL and create Beautiful Soup object...needs to know which URLs to get
page = requests.get('http://espn.go.com/college-football/boxscore?gameId=400763576')
tree = html.fromstring(page.content)
soup = BeautifulSoup(page.text, 'lxml')
statCatgs = ['gamepackage-passing','gamepackage-rushing','gamepackage-receiving','gamepackage-interceptions','gamepackage-kickReturns','gamepackage-kicking','gamepackage-punting']

for items in statCatgs:
    statCategories = soup.find(id=items)
    for cat in statCategories:
        for child in cat.children:
            players = child.find_all(findPlayer)
            for player in players:
                stats = player.find_parent('tr')
                for stat in stats.find_all(findPassingStats):
                    print stat['class']
                    print stat.get_text()





