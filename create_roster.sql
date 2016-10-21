DELIMITER $$

DROP PROCEDURE IF EXISTS `create_roster` $$
CREATE DEFINER=`user`@`%` PROCEDURE `create_roster`()
BEGIN

create table roster (
				week int not null,
				fant_team varchar(30) not null,
				player_name varchar(20) not null,
				pos varchar(2),
				is_starting varchar(1) not null,
				points_elig varchar(1) not null,
				points float,
				team varchar(20),
				opp varchar(20),
				primary key (week, fant_team, player_name);
            
END;$$

DELIMITER ;