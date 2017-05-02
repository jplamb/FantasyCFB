DELIMITER $$

DROP PROCEDURE IF EXISTS `get_team_def_points` $$
USE ffbdev$$
CREATE PROCEDURE get_team_def_points(IN VAR_WEEK INTEGER(2))
BEGIN

select x.player_name, pt.player_id,pt.total_points, x.is_starting, x.points_elig, x.fant_team
from roster x
inner join teams tm on tm.team = x.player_name
inner join points pt on pt.player_id = tm.team_id and x.week = pt.week
where x.pos = 'D' and pt.week = VAR_WEEK;
                
END;$$

DELIMITER ;