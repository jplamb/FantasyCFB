# Calculate player points
from dbConn import db_execute, db_dict_execute, check_table_exists
# Main method
def calc_all_player_points():
    
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
        week = 1
        game_log = get_player_game_log(player, week)

        if not game_log:
            continue

        for stat in game_log.keys():
            if stat in points_stats:
                total_points += points_stats[stat] * game_log[stat]
                #print stat, points_stats[stat], game_log[stat], total_points
                
        points_elig = get_player_elig(player, week)
        
        elig_points = 0
        unelig_points = 0
        
        if points_elig:
            elig_points = total_points
        else:
            unelig_points = total_points
            
        handle_player_points(player, week, total_points, elig_points, unelig_points)

def post_team_points(teams, week):
    for team in teams:
        select_sql = """
                select x.player_name, pt.player_id, pt.total_points, x.is_starting, x.points_elig
                from points pt
                inner join players play on play.player_id = pt.player_id
                inner join %s x on x.player_name = play.name and play.team = x.team
                where pt.week = %s
                """%(team, week)
                
        result = db_execute(select_sql)
        print team
        print_team_points(result, team)
    
def print_team_points(result, team):
    filename = team + 'stats.txt'
    f = open(filename,'w')
    
    f.write('Player, Player ID, Total Points, Starting, Eligible')

    for player in result:
        f.write('\n%s, %s, %s, %s, %s, %s'%(player[0], player[1], player[2], player[3], player[4], team))
    f.close()


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
			fg_made float not null default 0,
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
			primary key (effdt))
            """
    db_execute(create_string)

calc_all_player_points()
teams = ['Team_John_B', 'Team_Jack', 'Team_John_L', 'Team_Mike','Team_Scott','Team_Frankie']
post_team_points(teams, 1)