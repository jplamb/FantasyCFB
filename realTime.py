########################################################
#  Real time operations
#  10/11/16  John Lamb
########################################################

import datetime
import base64
from dbConn import Mysql 
def get_players_playing():
    now = datetime.datetime.now()
    
    date = now.strftime('%Y/%m/%d')
    time = now.strftime('%H:%M:%S')

    select_sql = """
            select * from schedule
            where gm_date <= curdate()
            """ 
    #print select_sql
    #print db_execute(select_sql)

connection = Mysql(host='localhost', user='appuser', password=base64.b64decode('YXBwdXNlcg=='), database='ffbdev')

#print connection.select('schedule','gm_date <= curdate()')
now = datetime.datetime.now()
end = now.strftime('%H:%M:%S')
start = (now - datetime.timedelta(hours = 4)).strftime('%H:%M:%S')
where = "gm_date = curdate() and gm_time between cast('%s' as time) and cast('%s' as time)" %(start, end)
subselect = "(select team from schedule where " + where + ')'
#print connection.select('players', 'team in ' + subselect, 'player_id')
#get_players_playing()
#connection = Mysql(host='localhost', user='appuser', password=base64.b64decode('YXBwdXNlcg=='), database='ffbdev')

print connection.call_store_procedure('check_table_exists','player_stats')