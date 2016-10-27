# Calculate player points
from dbConn import Mysql
import os

# Main method
def calc_all_player_points(week):
    
    ps_table_exists = __conn__.call_store_procedure('check_table_exists', 'points_stats')

    if not ps_table_exists:
        __conn__.call_store_procedure('create_points_stats')

    points_table_exists = __conn__.call_store_procedure('check_table_exists', 'points')
    
    if not points_table_exists:
        __conn__.call_store_procedure('create_points')
    

    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()

    # retrieve all player ids
    player_ids = get_player_ids()
    # for each player, calculate points
    for player in player_ids:
        print player[0]
        player = player[0]
        
        play_points = {}
        total_points = 0
        
        play_points['player_id'] = player
        play_points['week'] = week

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
        
        play_points['total_points'] = total_points  
        points_elig = get_player_elig(player, week)
        
        play_points['elig_points'] = 0
        play_points['unelig_points'] = 0
        
        if points_elig:
            play_points['elig_points'] = total_points
        else:
            play_points['unelig_points'] = total_points
            
        handle_player_points(**play_points)
    
    print_all_points(week)

def calc_team_def_points(week):
    ps_table_exists = __conn__.call_store_procedure('check_table_exists', 'points_stats')

    if not ps_table_exists:
        __conn__.call_store_procedure('create_points_stats')

    points_table_exists = __conn__.call_store_procedure('check_table_exists', 'points')
    
    if not points_table_exists:
        __conn__.call_store_procedure('create_points')
        
    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()
    
    teams = get_teams()
    print teams
    
    #for team, team_id in teams:
    for team in teams:
        team_name = team['team']
        team_id = team['team_id']
        print team_name, team_id
        
        play_points = {}
        total_points = 0
        
        play_points['player_id'] = team_id
        play_points['week'] = week
        
        victoryRes = get_team_points_allowed(team_name, week)
        if victoryRes:
            (win, game_points) = victoryRes[0]
            if 'OT' in game_points:
                game_points = game_points[:game_points.find('(OT)')].strip()
                
            (points_all1, points_all2) = game_points.split('-')

        print team_name, win, game_points
        
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
        
        int_caught = float(get_interceptions(team_name,week)[0][0])
        sacks = float(get_sacks(team_name, week)[0][0])
        fumbles = float(get_forced_fumbles(team_name, week)[0][0])
        int_td = float(get_int_td(team_name, week)[0][0])
        
        if int_caught:
            total_points += int_caught * points_stats['def_int']
        if sacks:
            total_points += sacks * points_stats['def_sacks']
        if fumbles:
            total_points += fumbles * points_stats['def_force_fmble']
        if int_td:
            total_points += int_td * points_stats['def_int_ret_td']
        
        play_points['total_points'] = total_points
        play_points['elig_points'] = 0
        play_points['unelig_points'] = 0
        
        team_elig = get_team_elig(team_name, week)
        
        if team_elig:
            play_points['elig_points'] = total_points
        else:
            play_points['unelig_points'] = total_points
        handle_player_points(**play_points)
        
def get_forced_fumbles(team, week):
    fumble_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is NULL)) and week = %s"""%(team, week)
            
    return __conn__.select('player_stats', fumble_where, 'sum(def_force_fmble)')[0][0]

def get_interceptions(team, week):
    inter_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null)) and week = %s"""%(team, week)
            
    return __conn__.select('player_stats', inter_where, 'sum(int_thrown)')[0][0]

def get_int_td(team, week):
    int_td_where = """team = '%s' and (position <> 'QB'
            or position is null)) and week = %s
            """%(team, week)
            
    return __conn__.select('player_stats',int_td_where, 'sum(def_int_ret_td)')[0][0]

def get_sacks(team, week):
    sack_where = """player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null)) and week = %s
            """%(team, week)
            
    return __conn__.select('player_stats', sack_where, 'sum(def_sacks)')[0][0]


def get_team_points_allowed(team, week):
    points_all_where = """player_id in
            (select player_id from players where team = '%s')
            and week = %s and victory is not null
            """%(team, week)
            
    points_all_select = ['victory', 'result']
    
    return __conn__.select('player_stats', points_all_where, *points_all_select)

def get_teams():
    teams_select = ['team', 'team_id']
    
    return __conn__.select('teams', None, *teams_select)


def post_team_points(week):
    result = __conn__.call_store_procedure('get_team_points', week)

    print_team_points(result, week)
    
    result_def = __conn__.call_store_procedure('get_team_def_points', week)

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
    elig_where = """week = %s and player_id in
                (select player_id from players where team = '%s') and opp in
                (select team from teams)
                """%(week, team)
    return __conn__.select('player_stats', elig_where, "'x'")[0]
                
def get_player_elig(player_id, week):
    elig_where = """player_id = %s and week = %s
                and opp in (select team from teams)
                """%(player_id, week)
    
    return __conn__.select('player_stats', elig_where, "'x'")

def get_player_game_log(player_id, week):
    check_where = """player_id = %s and week = %s
                """ %(player_id, week)
    if not __conn__.select('player_stats', check_where, "'x'"):
        return None
    
    dict_conn = Mysql(dict=True)
    
    play_where = 'player_id = %s and week = %s'%(player_id, week)
    game_log = dict_conn.select('player_stats', play_where, *'*')[0]
    return game_log

def get_points_stats_table():
    dict_conn = Mysql(dict=True)
    print dict_conn
    stats_where = "effdt = (select max(effdt) from points_stats)"
    return dict_conn.select('points_stats', stats_where, '*')[0]

def handle_player_points(**play_points):
    check_where = "player_id = %s and week = %s" %(play_points['player_id'], play_points['week'])

    if not __conn__.select('points', check_where, "'x'"):
        insert_player_points(**play_points)
    else:
        update_player_points(**play_points)

def insert_player_points(**play_points):
    __conn__.insert('points', **play_points)              

def update_player_points(**play_points):
    points_where = "player_id = %s and week = %s" %(play_points['player_id'], play_points['week'])
    play_points.pop('player_id', 0)
    play_points.pop('week', 0)
    __conn__.update('points', points_where, **play_points)
      
def get_player_ids():
    print __conn__
    return __conn__.select('players',None, 'player_id')

def input_points_stats():
    config = {}
    content = [line.rstrip('\n') for line in open('points-stats.txt')]
    
    for line in content:
        (stat, p) = line.split(':', 2)
        config[stat] = p.strip()
    
    insert_points_stats(**config)
    
def insert_points_stats(**config):
    row_where = "effdt = str_to_date(%s, '%%m/%%d/%%Y')" %(config['effdt'])
    
    if select.__conn__('points_stats', row_where, "'x'")[0]:
        __conn__.delete('points_stats', row_where)
        
    date = config.pop('effdt', None)
    
    __conn__.insert('points_stats', **config) 

def print_all_points(week):
    
    results = __conn__.call_store_procedure('print_all_points', week)

    filename = 'week' + str(week) + 'allstats.txt'
    f = open(filename,'w')
    
    if os.path.isfile(filename) and os.path.getsize(filename) == 0:
        f.write('Week, Fantasy Team, Total Points, Elig Points, Unelig Points, Player Name, Position, Team, Pass Yards, Pass TD, Int Thrown, Rush Yards, Rush TD, Rec Yards, Rec TD, FG 1-19, FG 20-29, FG 30-39, FG 40-49, FG 50+, FG Made, XP Made, XP Att, Def Sacks, Def Forced Fumbles, Def Int Ret TD')
    for row in results:
        f.write('\n')
        for stat in row:
            f.write('%s, '%(stat))
    f.close()

__conn__ = Mysql(dict=False)