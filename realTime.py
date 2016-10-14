########################################################
#  Real time operations
#  10/11/16  John Lamb
########################################################

import datetime
from dbConn import Mysql 
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

connection = Mysql()
print connection.select('schedule','where gm_date <= curdate()')
get_players_playing()