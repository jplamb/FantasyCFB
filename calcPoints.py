# Calculate player points
from dbConn import Mysql
import os

# Main method
def calc_all_player_points(week):
    conn = Mysql()
    
    ps_table_exists = conn.call_store_procedure('check_table_exists', 'points_stats')

    if not ps_table_exists:
        conn.call_store_procedure('create_points_stats')

    points_table_exists = conn.call_store_procedure('check_table_exists', 'points')
    
    if not points_table_exists:
        conn.call_store_procedure('create_points')
    

    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()[0]

    # retrieve all player ids
    player_ids = get_player_ids()
    # for each player, calculate points
    for player in player_ids:
        player = player[0]

        total_points = 0

        game_log = get_player_game_log(player, week)

        if not game_log:
            continue
        print player
        
        for stat in game_log.keys():
            if stat in points_stats and game_log[stat]:
                if isinstance(game_log[stat], basestring):
                    game_log[stat] = float(game_log[stat].split('/')[0]) 
                total_points += points_stats[stat] * game_log[stat]
                #print stat, points_stats[stat], game_log[stat], total_points
        
        if game_log['fg_made'] and len(game_log['fg_made']) > 1 and '/' in game_log['fg_made']:
            (made, att) = game_log['fg_made'].split('/')
            total_points += (float(att) - float(made)) * points_stats['fg_miss']
            
        points_elig = get_player_elig(player, week)
        
        elig_points = 0
        unelig_points = 0
        
        if points_elig:
            elig_points = total_points
        else:
            unelig_points = total_points
            
        handle_player_points(player, week, total_points, elig_points, unelig_points)
    
    print_all_points(week)

def calc_team_def_points(week):
    ps_table_exists = conn.call_store_procedure('check_table_exists', 'points_stats')

    if not ps_table_exists:
        conn.call_store_procedure('create_points_stats')

    points_table_exists = conn.call_store_procedure('check_table_exists', 'points')
    
    if not points_table_exists:
        conn.call_store_procedure('create_points')
        
    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()[0]
    
    teams = get_teams()

    for team, team_id in teams:
        print team
        total_points = 0
        
        victoryRes = get_team_points_allowed(team, week)
        if victoryRes:
            (win, game_points) = victoryRes[0]
            if 'OT' in game_points:
                game_points = game_points[:game_points.find('(OT)')].strip()
                
            (points_all1, points_all2) = game_points.split('-')

        print team, win, game_points
        
        if not win:
            points_all = 42
        elif win == 'W':
            points_all = int(points_all2)
        elif win == 'L':
            points_all = int(points_all1)
        else:
            points_all = 42
            
        if points_all == 0:
            total_points = points_stats['points_all_0']
        elif points_all <= 6:
            total_points = points_stats['points_all_6']
        elif points_all <= 13:
            total_points = points_stats['points_all_13']
        elif points_all <= 17:
            total_points = points_stats['points_all_17']
        elif points_all <= 27:
            total_points = points_stats['points_all_27']
        elif points_all <= 34:
            total_points = points_stats['points_all_34']
        elif points_all <= 45:
            total_points = points_stats['points_all_45']
        else:
            total_points = points_stats['points_all_plus']
        
        int_caught = float(get_interceptions(team,week)[0][0])
        sacks = float(get_sacks(team, week)[0][0])
        fumbles = float(get_forced_fumbles(team, week)[0][0])
        int_td = float(get_int_td(team, week)[0][0])
        
        if int_caught:
            total_points += int_caught * points_stats['def_int']
            print 'int',
            print total_points, int_caught
        if sacks:
            total_points += sacks * points_stats['def_sacks']
            print 'sacks',
            print total_points, sacks
        if fumbles:
            total_points += fumbles * points_stats['def_force_fmble']
            print 'fumbles',
            print total_points, fumbles
        if int_td:
            total_points += int_td * points_stats['def_int_ret_td']
            print 'int td',
            print total_points, int_td
        
        ePoints = 0
        uPoints = 0
        
        team_elig = get_team_elig(team, week)
        
        if team_elig:
            ePoints = total_points
        else:
            uPoints = total_points
        print team + ' saving'
        handle_player_points(team_id, week, total_points, ePoints, uPoints)
        
def get_forced_fumbles(team, week):
    fumble_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is NULL)) and week = %s"""%(team, week)
            
    return conn.select('player_stats', fumble_where, 'sum(def_force_fmble)')[0][0]

def get_interceptions(team, week):
    inter_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null)) and week = %s"""%(team, week)
            
    return conn.select('player_stats', inter_where, 'sum(int_thrown)')[0][0]

def get_int_td(team, week):
    int_td_where = """team = '%s' and (position <> 'QB'
            or position is null)) and week = %s
            """%(team, week)
            
    return conn.select('player_stats',int_td_where, 'sum(def_int_ret_td)')[0][0]

def get_sacks(team, week):
    sack_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null)) and week = %s
            """%(team, week)
            
    return conn.select('player_stats', sack_where, 'sum(def_sacks)')[0][0]


def get_team_points_allowed(team, week):
    points_all_where = """player_id in
            (select player_id from players where team = '%s')
            and week = %s and victory is not null
            """%(team, week)
            
    points_all_select = ['victory', 'result']
    
    return conn.select('player_stats', points_all_where, *points_all_select)[0]

def get_teams():
    teams_select = ['team', 'team_id']
    
    return conn.select('teams', where=None, *teams_select)


def post_team_points(week):
    result = conn.call_store_procedure('get_team_points', week)

    print_team_points(result, week)
    
    result_def = conn.call_store_procedure('get_team_def_points', week)

    print_team_points(result_def, week)
    
def print_team_points(result, week):
    filename = 'week' + str(week) + '.txt'
    f = open(filename,'a')
    
    if os.path.isfile(filename) and os.path.getsize(filename) == 0:
        f.write('Player, Player ID, Total Points, Starting, Eligible, Fant Team')

    for player in result:
        f.write('\n%s, %s, %s, %s, %s, %s'%(player[0], player[1], player[2], player[3], player[4], player[5]))
    f.close()

def get_team_elig(team, week):
    select_sql = """
                select (1) from player_stats where week = %s and player_id in
                (select player_id from players where team = '%s') and opp in
                (select team from teams)
                """%(week, team)
    return db_execute(select_sql)
                
def get_player_elig(player_id, week):
    select_sql = """
                select (1) from player_stats
                where player_id = %s and week = %s
                and opp in (select team from teams)
                """%(player_id, week)
    return db_execute(select_sql)

def get_player_game_log(player_id, week):
    check_row_sql = """select (1) from player_stats
                where player_id = %s and week = %s
                """ %(player_id, week)
    if not db_execute(check_row_sql):
        return None
    
    select_sql = """
        select * from player_stats
        where player_id = %s and week = %s
        """%(player_id, week)
        
    game_log = db_dict_execute(select_sql)[0]

    return game_log

def get_points_stats_table():
    select_sql = """
                select * from points_stats where effdt =
                    (select max(effdt) from points_stats)
                """
    return db_dict_execute(select_sql)
        
def handle_player_points(player_id, week, tPoints, ePoints, uPoints):
    check_row_sql = """
            select (1) from points
            where player_id = %s and week = %s
            """%(player_id, week)

    if not db_execute(check_row_sql):
        insert_player_points(player_id, week, tPoints, ePoints, uPoints)
    else:
        update_player_points(player_id, week, tPoints, ePoints, uPoints)

def insert_player_points(player_id, week, tPoints, ePoints, uPoints):
    insert_sql = """
                insert into points(
                week,
                player_id,
                total_points,
                elig_points,
                unelig_points)
                values
                (%s, %s, %s, %s, %s)
                """%(week, player_id, tPoints, ePoints, uPoints)
    db_execute(insert_sql)
                

def update_player_points(player_id, week, tPoints, ePoints, uPoints):
    update_sql = """
                update points
                set total_points = %s,
                elig_points = %s,
                unelig_points = %s
                where player_id = %s and week = %s
                """%(tPoints, ePoints, uPoints, player_id, week)
    db_execute(update_sql)
    
def get_player_ids():
    select_sql = """
            select player_id from players
            """
    return db_execute(select_sql)

def input_points_stats():
    dict = {}
    content = [line.rstrip('\n') for line in open('points-stats.txt')]
    
    for line in content:
        (stat, p) = line.split(':', 2)
        dict[stat] = p.strip()
    
    insert_points_stats(dict)
    
def insert_points_stats(dict):
    check_row_exists_sql = """
                select (1) from points_stats
                where effdt = str_to_date(%s, '%%m/%%d/%%Y')
                """ %(dict['effdt'])
    
    if db_execute(check_row_exists_sql):
        delete_sql = """ delete from points_stats
                    where effdt = str_to_date(%s, '%%m/%%d/%%Y')"""%(dict['effdt'])
        db_execute(delete_sql)
        
    date = dict.pop('effdt', None)

    insert_sql = """
            insert into points_stats (effdt,"""
    
    for k in dict.keys():
        insert_sql += k + ','
    
    insert_sql = insert_sql[:-1]
    insert_sql += """) values (str_to_date('%s', '%%m/%%d/%%Y'),"""%(date)
    
    
    for k in dict.keys():
        insert_sql += dict[k] + ','
        
    insert_sql = insert_sql[:-1] + ')'

    db_execute(insert_sql)
    

def print_all_points(week):
    
    select_sql = """
            select pt.week,
                case when rost.fant_team is NULL then ' ' else rost.fant_team end,
                pt.total_points, pt.elig_points, pt.unelig_points,
                play.name, play.position, play.team, st.pass_yards, st.pass_td,
                st.int_thrown, st.rush_yards, st.rush_td, st.rec_yards, st.rec_td,
                st.fg_1_19, st.fg_20_29, st.fg_30_39, st.fg_40_49, st.fg_50_plus,
                st.fg_made, st.xp_made, st.xp_att, st.def_sacks, st.def_force_fmble,
                st.def_int_ret_td
            from points pt
            inner join player_stats st on st.player_id = pt.player_id and pt.week = st.week
            left join roster rost on rost.player_name = st.player_name and rost.week = st.week
            left join players play on play.player_id = st.player_id
            where pt.week = %s
            """%(week)
    
    results = db_execute(select_sql)
    
    filename = 'week' + str(week) + 'allstats.txt'
    f = open(filename,'w')
    
    if os.path.isfile(filename) and os.path.getsize(filename) == 0:
        f.write('Week, Fantasy Team, Total Points, Elig Points, Unelig Points, Player Name, Position, Team, Pass Yards, Pass TD, Int Thrown, Rush Yards, Rush TD, Rec Yards, Rec TD, FG 1-19, FG 20-29, FG 30-39, FG 40-49, FG 50+, FG Made, XP Made, XP Att, Def Sacks, Def Forced Fumbles, Def Int Ret TD')
    for row in results:
        f.write('\n')
        for stat in row:
            f.write('%s, '%(stat))
    f.close()
    
#print_all_points(1)
conn = Mysql()
print post_team_points(7)