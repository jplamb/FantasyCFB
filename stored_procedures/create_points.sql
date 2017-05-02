DELIMITER $$

DROP PROCEDURE IF EXISTS `create_points` $$
CREATE DEFINER=`user`@`%` PROCEDURE `create_points`()
BEGIN

create table points (
        week int not null,
        player_id int not null,
        total_points float not null,
        elig_points float not null,
        unelig_points float not null,
        primary key (week, player_id)
         );
            
            
END;$$

DELIMITER ;