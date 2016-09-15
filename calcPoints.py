# Calculate player points
from dbConn import db_execute, db_dict_execute, check_table_exists
import os

# Main method
def calc_all_player_points(week):
    
    # check if both the points for stat and player points tables exists
    if not check_table_exists('points_stats'):
        create_points_stats_table()
    if not check_table_exists('points'):
        create_points_table()
        
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
    # check if both the points for stat and player points tables exists
    if not check_table_exists('points_stats'):
        create_points_stats_table()
    if not check_table_exists('points'):
        create_points_table()
        
    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()[0]
    
    teams = get_teams()

    for team, team_id in teams:
        print team
        total_points = 0
        
        game_results = get_team_result(team, week)
        
        if not game_results:
            continue
        
        game_result, opp = game_results[0]

        for x in range(len(game_results)):
            if '-' not in game_result:
                game_result, opp = game_results[x]
        
        x = 0
        while x < len(game_results) and '-' not in game_result:
            game_result, opp = game_results[x]
            print game_result
            x+=1
        #if '-' not in game_result:
        #    continue
        (points_all1, points_all2) = game_result.split('-')
        
        victory = ''
        while victory != 'Y' and victory != 'N':
            victory = raw_input('Did %s win?\n'%(team)).strip().upper()
        
        if victory == 'Y':
            points_all = points_all2
        else:
            points_all = points_all1
            
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
        
        int_caught = float(get_interceptions(team)[0][0])
        sacks = float(get_sacks(team)[0][0])
        fumbles = float(get_forced_fumbles(team)[0][0])
        
        if int_caught:
            total_points += int_caught * points_stats['def_int']
        if sacks:
            total_points += sacks * points_stats['def_sacks']
        if fumbles:
            total_points += fumbles * points_stats['def_force_fmble']
        
        ePoints = 0
        uPoints = 0
        
        team_elig = get_team_elig(team, week)
        
        if team_elig:
            ePoints = total_points
        else:
            uPoints = total_points
        print team + ' saving'
        handle_player_points(team_id, week, total_points, ePoints, uPoints)
        
def get_forced_fumbles(team):
    select_sql = """
            select sum(def_force_fmble) from player_stats where player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is NULL))
            """%(team)
    return db_execute(select_sql)

def get_interceptions(team):
    select_sql = """
            select sum(int_thrown) from player_stats where player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null))
            """%(team)
    return db_execute(select_sql)

def get_sacks(team):
    select_sql = """
            select sum(def_sacks) from player_stats where player_id in
            (select player_id from players where team = '%s' and (position <> 'QB'
            or position is null))
            """%(team)
    return db_execute(select_sql)
        
def get_team_result(team, week):
    select_sql = """
            select result,opp from player_stats where player_id in
            (select player_id from players where team = '%s') and week = %s
            """%(team, week)
    return db_execute(select_sql)

def get_team_victory(team, week, opp):
    select_sql = """
            select status from schedule where team = '%s'
            and opp = '%s'
            """%(team, opp)
    return db_execute(select_sql)
    
def get_teams():
    select_sql = """
            select team, team_id from teams
            """
    return db_execute(select_sql)

def post_team_points(teams, week):
    for team in teams:
        select_sql = """
                select x.player_name, pt.player_id, pt.total_points, x.is_starting, x.points_elig
                from points pt
                inner join players play on play.player_id = pt.player_id
                inner join %s x on x.player_name = play.name and play.team = x.team
                and x.week = pt.week
                where pt.week = %s                
                """%(team, week)
                
        result = db_execute(select_sql)
        print team
        print_team_points(result, team)
        select_sql = """
                select x.player_name, pt.player_id,pt.total_points, x.is_starting, x.points_elig
                from %s x
                inner join teams tm on tm.team = x.player_name
                inner join points pt on pt.player_id = tm.team_id and x.week = pt.week
                where x.pos = 'D' and pt.week = %s
                """%(team, week)
        result = db_execute(select_sql)
        print_team_points(result, team, week)
    
def print_team_points(result, team, week):
    filename = 'week' + str(week) + '.txt'
    f = open(filename,'a')
    
    if os.path.isfile(filename) and os.path.getsize(filename) == 0:
        f.write('Player, Player ID, Total Points, Starting, Eligible')

    for player in result:
        f.write('\n%s, %s, %s, %s, %s, %s'%(player[0], player[1], player[2], player[3], player[4], team))
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

def create_points_table():
    create_string = """
        create table points (
        week int not null,
        player_id int not null,
        total_points float not null,
        elig_points float not null,
        unelig_points float not null,
        primary key (week, player_id)
         )"""
    db_execute(create_string)

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
    
    
def create_points__stats_table():
    create_string = """create table points_stats (
            effdt date not null,
			completions float not null default 0,
			pass_att float not null default 0,
			pass_yards float not null default 0,
			compl_pct float not null default 0,
			pass_long float not null default 0,
			pass_td float not null default 0,
			int_thrown float not null default 0,
			pass_rate float not null default 0,
			raw_qbr float not null default 0,
			adj_qbr float not null default 0,
			rush_att float not null default 0,
            qb_rush float not null default 0,
			rush_yards float not null default 0,
			rush_avg float not null default 0,
			rush_long float not null default 0,
			rush_td float not null default 0,
			receptions float not null default 0,
			rec_yards float not null default 0,
			rec_avg float not null default 0,
			rec_long float not null default 0,
			rec_td float not null default 0,
			fg_1_19 float not null default 0,
			fg_20_29 float not null default 0,
			fg_30_39 float not null default 0,
			fg_40_49 float not null default 0,
			fg_50_plus float not null default 0,
			fg_miss float not null default 0,
			fg_pct float not null default 0,
			fg_long float not null default 0,
			xp_made float not null default 0,
			xp_miss float not null default 0,
			kick_points float not null default 0,
			def_tot_tack float not null default 0,
			def_unassist_tack float not null default 0,
			def_assist_tack float not null default 0,
			def_sacks float not null default 0,
			def_force_fmble float not null default 0,
			def_int_ret_yrds float not null default 0,
			def_int_ret_avg float not null default 0,
			def_int_ret_long float not null default 0,
			def_int_ret_td float not null default 0,
			def_pass_defend float not null default 0,
			punt_total float not null default 0,
			punt_avg float not null default 0,
			punt_long float not null default 0,
			punt_total_yrds float not null default 0,
            points_all_0 float not null default 0,
            points_all_6 float not null default 0,
            points_all_13 float not null default 0,
            points_all_17 float not null default 0,
            points_all_27 float not null default 0,
            points_all_34 float not null default 0,
            points_all_45 float not null default 0,
            points_all_plus float not null default 0,
            def_int float not null default 0,
			primary key (effdt))
            """
    db_execute(create_string)

def print_all_points(week):
    select_sql = """
            select * from points pt
            inner join player_stats st on st.player_id = pt.player_id and pt.week = st.week
            where pt.week = %s
            """%(week)
    
    results = db_execute(select_sql)
    
    filename = 'week' + str(week) + 'allstats.txt'
    f = open(filename,'w')
    
    if os.path.isfile(filename) and os.path.getsize(filename) == 0:
        f.write('Week, Player ID, Total Points, Elig Points, Unelig Points, week, player id, Game Date, Player Name, Opponent, Result, Pass Compl, Pass Att, Pass Yards, Compl Pct, Pass Long, Pass TD, Int Thrown, Pass Rate, Raw QBR, Adj QBR, Rush Att, Rush Yards, Rush Avg, Rush Long, Rush TD, Rec Receptions, Rec Yards, Rec Avg, Rec Long, Rec TD, FG 1-19, FG 20-29, FG 30-39, FG 40-49, FG 50+, FG Made, FG Pct, FG Long, XP Made, XP Att, Kick Points, Def Tackles, Def Unassist Tackles, Def Ass Tackles, Def Sacks, Def Forced Fumbles, Def Int Ret Yards, Def Int Ret Avg, Def Int Ret Long, Def Int Ret TD, Def Pass Defend, Punt Total, Punt Avg, Punt Total, Punt Total Yards')
    for row in results:
        f.write('\n')
        for stat in row:
            f.write('%s, '%(stat))
    f.close()
    
    
