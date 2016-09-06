# Calculate player points

# Main method
def calc_all_player_points():
    
    # check if both the points for stat and player points tables exists
    if not check_table_exists('points_stats'):
        create_points_stats_table()
    if not check_table_exists('points'):
        create_points_table()
    
    # retrieve the points for stats table (as dict)
    points_stats = get_points_stats_table()
    
    # retrieve all player ids
    player_ids = get_player_ids()
    
    # for each player, calculate points
    for player in player_ids:
        total_points = 0
        
        gLog = get_player_game_log(player, week)
        
        if not gLog:
            continue
        
        for stat in game_log.keys():
            total_points += points_stats[stat] * game_log[stat]

        if points_elig:
            elig_points = total_points
        else:
            unelig_points = total_points
        handle_player_points(player_id, week, total_points, elig_points, unelig_points)
        
def get_player_game_log(player_id, week):
    check_row_sql = """select (1) from player_stats
                where player_id = %s and week = %s
                """ %(player_id, week)
    if not db_execute(check_row_sql):
        return None
    
    select_sql = """
        select * from player_stats
        where player_id = %s and week = %s
        """
        
    return db_dict_execute(select_sql)
        
def handle_player_points(player_id, week, tPoints, ePoints, uPoints):
    check_row_sql = """
            select (1) from points
            where player_id = %s and week = %s"""
    
    if not db_execute(check_row_sql):
        insert_player_points(player_id, week, tPoints, ePoints, uPoints)
    else:
        update_player_points(player_id, week, tPoints, ePoints, uPoints)

def insert_player_points(player_id, week, tPoints, ePoints, uPoints):
    pass

def update_player_points(player_id, week, tPoints, ePoints, uPoints):
    pass
    
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
    
    f.open('points-stats.txt','r')
    
    # read in comma deliminated file of points per stat

def create_points__stats_table():
    create_string = """create table points_stats (
            effdt date note null,
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
			xp_att float not null default 0,
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
			primary key (effdt)
            """
    