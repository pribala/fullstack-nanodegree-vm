-- Table definitions for the tournament project.

-- Drop any existing database
-- DROP database tournament;
DROP DATABASE tournament;

-- Create tournament database
-- CREATE database tournament;
CREATE DATABASE tournament;

-- Connect to the database
\c tournament;

--Create the database schema
CREATE TABLE players (
	player_id SERIAL PRIMARY KEY,
	name text NOT NULL
);	

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(player_id),
	loser INTEGER REFERENCES players(player_id)
);	

-- Create a view to display the player_id and their total wins
CREATE OR REPLACE VIEW player_wins (player, wins) AS 
SELECT players.player_id, COUNT(matches.winner) AS wins FROM players LEFT JOIN matches 
ON player_id = winner 
GROUP BY player_id ORDER BY wins DESC;

-- Create a view to display the player_id and the total matches played by them
CREATE OR REPLACE VIEW  player_matches (player, matches) AS 
SELECT players.player_id, COUNT(matches.match_id) 
FROM players LEFT JOIN matches 
ON players.player_id = matches.winner OR players.player_id = matches.loser 
GROUP BY player_id ORDER BY player_id;

-- Create a view to display the player standings
CREATE OR REPLACE VIEW player_standings (player_id, name, wins, matches) AS
SELECT players.player_id, players.name, player_wins.wins, player_matches.matches
FROM players, player_matches, player_wins
WHERE players.player_id = player_matches.player AND players.player_id = player_wins.player
ORDER BY wins DESC; 

-- Create a view to pair the players as per their rank
CREATE OR REPLACE VIEW swiss_pairs (id1, name1, id2, name2) AS
WITH ranked_players AS 
    (SELECT player_id, name, ROW_NUMBER() OVER(ORDER BY wins) AS rank
    FROM player_standings)
SELECT player1.player_id, player1.name, player2.player_id, player2.name
    FROM ranked_players as player1
    JOIN ranked_players as player2
    ON player1.rank=player2.rank-1
    WHERE player1.rank % 2 = 1;

