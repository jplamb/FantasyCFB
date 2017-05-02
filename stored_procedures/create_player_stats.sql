DELIMITER $$

DROP PROCEDURE IF EXISTS `create_player_stats` $$
CREATE DEFINER=`user`@`%` PROCEDURE `create_player_stats`()
BEGIN

create table player_stats (
			week int not null,
			player_id int not null,
			game_date varchar(10),
			player_name varchar(30),
			opp varchar(30),
			result varchar(20),
			victory varchar(1),
			completions int not null default 0,
			pass_att int not null default 0,
			pass_yards int not null default 0,
			compl_pct float not null default 0,
			pass_long int not null default 0,
			pass_td int not null default 0,
			int_thrown int not null default 0,
			pass_rate float not null default 0,
			raw_qbr float not null default 0,
			adj_qbr float not null default 0,
			rush_att int not null default 0,
			rush_yards int not null default 0,
			rush_avg float not null default 0,
			rush_long int not null default 0,
			rush_td int not null default 0,
			receptions int not null default 0,
			rec_yards int not null default 0,
			rec_avg float not null default 0,
			rec_long int not null default 0,
			rec_td int not null default 0,
			fg_1_19 int not null default 0,
			fg_20_29 int not null default 0,
			fg_30_39 int not null default 0,
			fg_40_49 int not null default 0,
			fg_50_plus int not null default 0,
			fg_made int not null default 0,
			fg_pct float not null default 0,
			fg_long int not null default 0,
			xp_made int not null default 0,
			xp_att int not null default 0,
			kick_points int not null default 0,
			def_tot_tack int not null default 0,
			def_unassist_tack int not null default 0,
			def_assist_tack int not null default 0,
			def_sacks float not null default 0,
			def_force_fmble int not null default 0,
			def_int_ret_yrds int not null default 0,
			def_int_ret_avg int not null default 0,
			def_int_ret_long int not null default 0,
			def_int_ret_td int not null default 0,
			def_pass_defend int not null default 0,
			punt_total int not null default 0,
			punt_avg float not null default 0,
			punt_long int not null default 0,
			punt_total_yrds int not null default 0,
			primary key (week, player_id));
            
END;$$

DELIMITER ;