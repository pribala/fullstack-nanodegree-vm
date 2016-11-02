#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=extra_credit")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from matches"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from players"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from tournaments"
    db_cursor.execute(query)
    conn.commit()
    conn.close()

	
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "select count(*) from players"
    db_cursor.execute(query)
    total_players = db_cursor.fetchone()
    conn.close()
    return (int(total_players[0]))


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    is handled by the SQL database schema, not in the Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    db_cursor = conn.cursor()
    db_cursor.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    conn.close()
	

def reportMatch(tour_id, winner, loser, draw):
    """Records the outcome of a single match between two players for a single tournament.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
	  tour_id: the id number of the tournament for the current match
	  draw: states whether a match is a draw or not
    """
    conn = connect()
    db_cursor = conn.cursor()
    db_cursor.execute("insert into matches (tour_id, winner, loser, draw) values(%s, %s, %s, %s)",
                      (tour_id, winner, loser, draw))
    conn.commit()
    conn.close()


def addTournament(name):
    """ Adds a new tournament to the database.
	
	Args:
	   name: name of the tournament
	"""
    conn = connect()
    db_cursor = conn.cursor()
    db_cursor.execute("insert into tournaments (name) values(%s) RETURNING tour_id",
                      (name,))
    tid = db_cursor.fetchone()[0]					  
    conn.commit()
    conn.close()
    return (int(tid))	


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins for a given tournament.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, tour_id, wins, matches, draws):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
		tour_id: the tournament id of the current tournament
        wins: the number of matches the player has won in this tournament
        matches: the number of matches the player has played in this tournament
		draws: the number of tied matches
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "select player_id, name, tour_id, wins, matches, draws from player_standings"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    conn.close
    return result
	

def swissPairings():
    """Returns a list of pairs of players for the next round of a match based on ranking in each tournament.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "select id1, name1, id2, name2, tour_id from swiss_pairs"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    conn.close
    return result
