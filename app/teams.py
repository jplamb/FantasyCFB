from dbConn import Mysql
from lxml import html
from bs4 import BeautifulSoup
import requests

# Handle schedule updates
# input date as string, opp as string, status as string, and time as string
def record_team(team_name, team_id):
    if not __conn.call_store_procedure('check_table_exists', 'teams'):
        __conn.call_store_procedure('create_teams')
    
    row_where = 'team_id = %s'%(team_id)
    values = {}
    values['team'] = team_name
    values['team_id'] = team_id
    
    if __conn.select('teams', row_where, "'x'"):
        update_team(**values)
    else:
        insert_team(**values)

# Add team to table      
def insert_team(**kwargs):
    __conn.insert('teams', **kwargs)

# Update team row 
def update_team(**kwargs):
    values = kwargs
    
    update_where = 'team_id = %s'%(values['team_id'])
    
    values.pop('team_id', 0)
    
    __conn.update('teams', update_where, **values)

    
__conn = Mysql()