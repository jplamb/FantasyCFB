########################################################
#  Real time operations
#  10/11/16  John Lamb
########################################################

import datetime
from dbConn import db_execute, close_db, open_db_connection
def get_players_playing():
    now = datetime.datetime.now()
    
    date = now.strftime('%Y/%m/%d')
    time = now.strftime('%H:%M:%S')

    select_sql = """
            select * from schedule
            where gm_date <= curdate()
            """ 
    print select_sql
    print db_execute(select_sql)
    
open_db_connection(False)
get_players_playing()