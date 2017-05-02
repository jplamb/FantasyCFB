DELIMITER $$

DROP PROCEDURE IF EXISTS `print_all_points` $$
USE ffbdev$$
CREATE PROCEDURE print_all_points(IN VAR_WEEK INTEGER(2))
BEGIN

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
            where pt.week = VAR_WEEK;
                
END;$$

DELIMITER ;