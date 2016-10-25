import random
from tournament import connect
from tournament import reportMatch
#from tournament_test import testDelete

the_players = [
    (1, 'Jeff'),
	(2, 'Adarsh'),
	(3, 'Amanda'),
	(4, 'Eduardo'),
	(5, 'Philip')
]

def registerPlayerUpdated(player_id, name):
    """Add a player to the tournament database."""
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players(player_id, name) VALUES (%s, %s)"
    db_cursor.execute(query,(player_id,name))
    db.commit()
    db.close()

def createRandomMatches(player_list, num_matches):
    num_players = len(player_list)
    for i in xrange(num_matches):
        print 'match %s' % (i + 1)
        player1_index = random.randint(0, num_players - 1)
        player2_index = random.randint(0, num_players - 1)		
        if player2_index == player1_index:
            player2_index = (player1_index + 1) % num_players
        winner_id = player_list[player1_index][0]
        winner_name = player_list[player1_index][1]
        loser_id = player_list[player2_index][0]
        loser_name = player_list[player2_index][1]
        reportMatch(winner_id, loser_id)
        print "%s (id=%s) beat %s (id=%s)" % (winner_name,winner_id,loser_name,loser_id)		

def setup_players_and_matches():
    #testDelete()
    for player in the_players:
        registerPlayerUpdated(player[0], player[1])
    createRandomMatches(the_players, 100)		
	
if __name__ == '__main__':
    setup_players_and_matches()	