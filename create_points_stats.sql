DELIMITER $$

DROP PROCEDURE IF EXISTS `create_points_stats` $$
CREATE DEFINER=`user`@`%` PROCEDURE `create_points_stats`()
BEGIN

create table points_stats (
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
			primary key (effdt));
            
            
END;$$

DELIMITER ;