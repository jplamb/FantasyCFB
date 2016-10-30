DELIMITER $$

DROP PROCEDURE IF EXISTS `create_players` $$
USE ffbdev$$
CREATE PROCEDURE create_players()
BEGIN

create table players(
			player_id int not null,
			name varchar(30),
			url varchar(150),
			team varchar(30),
			position varchar(3),
			primary key (player_id));
                
END;$$

DELIMITER ;