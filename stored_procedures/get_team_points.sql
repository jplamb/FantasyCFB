DELIMITER $$

DROP PROCEDURE IF EXISTS `get_team_points` $$
USE ffbdev$$
CREATE PROCEDURE get_team_points(IN VAR_WEEK INTEGER(2))
BEGIN

select x.player_name, pt.player_id, pt.total_points, x.is_starting, x.points_elig, x.fant_team
                from points pt
                inner join players play on play.player_id = pt.player_id
                inner join roster x on x.player_name = play.name and play.team = x.team
                and x.week = pt.week
                where pt.week = VAR_WEEK;
                
END;$$

DELIMITER ;