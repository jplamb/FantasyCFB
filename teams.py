from dbConn import Mysql
from lxml import html
from bs4 import BeautifulSoup
import requests

# Crete table
# inputs: table_name as string
def create_table():		

    create_sql = """
            create table teams (
            team varchar(20) not null,
            team_id int not null,
            primary key(team)
            )"""
            
    db_execute(create_sql)

# Handle schedule updates
# input date as string, opp as string, status as string, and time as string
def record_team(team_name, team_id):
    if not check_table_exists('teams'):
        create_table()
        
    row_exists_sql = """
        select (1)
        from teams
        where team_id = %s
        """ % (team_id)
    
    if db_execute(row_exists_sql):
        update_team(team_name, team_id)
    else:
        insert_team(team_name, team_id)

# Add team to table      
def insert_team(team_name, team_id):
    insert_sql = """
            insert into teams (
            team,
            team_id
            )
            values (
            '%s',
            %s
            )
            """ %(team_name, team_id)
    print insert_sql
    db_execute(insert_sql)

# Update team row 
def update_team(team_name, team_id):

    update_sql = """
            update teams 
            set 
            team = '%s'
            where
            team_id = %s 
            """ % (team_name, team_id)				
    db_execute(update_sql)