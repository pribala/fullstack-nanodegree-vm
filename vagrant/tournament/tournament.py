#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    #return psycopg2.connect("dbname=tournament")
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error connecting to the database")
	

def deleteMatches():
    """Remove all the match records from the database."""
    conn, db_cursor = connect()
    query = "delete from matches"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, db_cursor = connect()
    query = "delete from players"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, db_cursor = connect()
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
    conn, db_cursor = connect()
    db_cursor.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, db_cursor = connect()
    query = "select player_id, name, wins, matches from player_standings"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    conn.close
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, db_cursor = connect()
    db_cursor.execute("insert into matches (winner, loser) values(%s, %s)",
                      (winner, loser,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

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
    conn, db_cursor = connect()
    query = "select id1, name1, id2, name2 from swiss_pairs"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    conn.close
    return result
