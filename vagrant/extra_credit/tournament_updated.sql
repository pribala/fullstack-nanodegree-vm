-- Create database 
CREATE DATABASE extra_credit;

-- Connect to the database
\c extra_credit;

-- Create a table for tournament details 
CREATE TABLE tournaments (
	tour_id SERIAL PRIMARY KEY,
	name text NOT NULL
);

-- Create a table for player details
CREATE TABLE players (
	player_id SERIAL PRIMARY KEY,
	name text NOT NULL
);

-- Create a table for match details
CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	tour_id INTEGER REFERENCES tournaments (tour_id),
	winner INTEGER REFERENCES players (player_id),
	loser INTEGER REFERENCES players (player_id),
	draw BOOLEAN DEFAULT FALSE
);

-- Create a view to display the player_id and their total wins in each tournament
CREATE OR REPLACE VIEW player_wins (tour_id, player, wins) AS 
SELECT tour_id, players.player_id, COUNT(matches.winner) AS wins FROM players LEFT JOIN matches 
ON player_id = winner AND draw != 't'
GROUP BY tour_id, player_id ORDER BY wins DESC;

-- Create a view to display the player_id and the total matches played by them
CREATE OR REPLACE VIEW  player_matches (tour_id, player, matches) AS 
SELECT tour_id, players.player_id, COUNT(matches.match_id) 
FROM players LEFT JOIN matches 
ON players.player_id = matches.winner OR players.player_id = matches.loser 
GROUP BY tour_id, player_id ORDER BY tour_id, player_id;

-- Create a view to display the player_id and their total draws
CREATE OR REPLACE VIEW player_draws (tour_id, player, draws) AS 
SELECT tour_id, players.player_id, COUNT(matches.draw) AS draws FROM players LEFT JOIN matches 
ON draw = 't' AND (player_id = winner  OR player_id = loser)
GROUP BY tour_id, player_id;

-- Create a view to display the player standings
CREATE OR REPLACE VIEW player_standings (player_id, name, tour_id, matches, wins, draws) AS
SELECT players.player_id, players.name, COALESCE(player_matches.tour_id,0), player_matches.matches, 
COALESCE(player_wins.wins,0) AS wins, COALESCE(player_draws.draws,0) AS draws 
FROM player_matches LEFT JOIN player_wins ON (player_matches.tour_id = player_wins.tour_id AND player_matches.player = player_wins.player)
LEFT JOIN player_draws ON (player_matches.tour_id = player_draws.tour_id AND player_matches.player = player_draws.player)
LEFT JOIN players ON (player_matches.player = players.player_id)
ORDER BY player_matches.tour_id; 

-- Create a view for ranking players, to calculate rank we subtract half of the cumulative draws of a player
-- from their cumulative wins and take the absolute value
CREATE OR REPLACE VIEW player_ranks (player_id, name, tour_id, ranking) AS
SELECT player_id, name, tour_id,(ABS(wins::FLOAT - draws::FLOAT/2)) AS ranking
FROM player_standings
ORDER BY tour_id,ranking DESC ;

-- Create a view to pair the players as per their rank - modify the function to pair rows
CREATE OR REPLACE VIEW swiss_pairs (id1, name1, id2, name2, tour_id) AS
WITH ranked_players AS 
    (SELECT player_id, name, tour_id, ROW_NUMBER() OVER(PARTITION BY tour_id ORDER BY ranking DESC) AS rank
    FROM player_ranks)
SELECT player1.player_id, player1.name, player2.player_id, player2.name, player1.tour_id
    FROM ranked_players as player1
    JOIN ranked_players as player2
    ON player1.rank=player2.rank-1
    WHERE player1.rank % 2 = 1 AND player1.tour_id = player2.tour_id;

	