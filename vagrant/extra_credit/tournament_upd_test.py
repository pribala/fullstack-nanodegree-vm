#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they cover the majority of cases.
#


from tournament_upd import *

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches()
    deleteTournaments()		
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."  # noqa
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))  # noqa
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))  # noqa
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."  # noqa


def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches()
    deleteTournaments()		
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even "
                         "before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 6:
        raise ValueError("Each playerStandings row should have six columns.")
    [(id1, name1,tour_id1, wins1, matches1, draws1), (id2, name2,tour_id2, wins2, matches2, draws2)] = standings
    if tour_id1 != 0 or tour_id2 != 0 or matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or draws1 !=0 or draws2 !=0:
        raise ValueError(
            "Newly registered players should have no tournaments or matches or wins or draws.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."  # noqa
	
def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches()
    deleteTournaments()	 	
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    print (id1, id2, id3, id4)
    tid = addTournament("US Open")	
    reportMatch(tid, id1, id2, 'FALSE')
    reportMatch(tid, id3, id4, 'TRUE')
    standings = playerStandings()
    for (i, n,t, w, m, d) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            if d !=1:
                raise ValueError("Each match winner should have one win or draw recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser or in case of tied match should have zero "
                             "wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches()
    deleteTournaments()		
    standings = playerStandings()
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of "
                         "players in standings.")
    for (i, n,t, w, m, d) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have "
                             "zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have "
                             "zero wins recorded.")
        if t != 0:
            raise ValueError("After deleting tournaments, there should be no records in tournament table.")
        if d != 0:
            raise ValueError("After deleting matches players should have zero draws recorded.")		
    print "8. After match deletion, player standings are properly reset.\n9. Matches and Tournaments are properly deleted."  # noqa

def testPairings():
    """
    Test that pairings are generated properly both before and after match
    reporting.
    """
    deleteMatches()
    deleteTournaments()	
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))  # noqa
    tid = addTournament("US Open")
    reportMatch(tid, id1, id2, 'FALSE')
    reportMatch(tid, id3, id4, 'TRUE')
    reportMatch(tid, id5, id6, 'FALSE')
    reportMatch(tid, id7, id8, 'FALSE')
    tid = addTournament("Wimbeldon")
    reportMatch(tid, id1, id2, 'FALSE')
    reportMatch(tid, id3, id4, 'FALSE')	
    pairings = swissPairings()
    if len(pairings) != 6:
        raise ValueError(
            "For eight players in 2 tournaments, swissPairings should return 6 pairs. Got {pairs}".format(pairs=len(pairings)))  # noqa
    [(pid1, pname1, pid2, pname2, tid), (pid3, pname3, pid4, pname4, tid), (pid5, pname5, pid6, pname6, tid), (pid7, pname7, pid8, pname8, tid), (pid9, pname9, pid10, pname10, tid), (pid11, pname11, pid12, pname12, tid)] = pairings  # noqa
    possible_pairs = set([frozenset([id1, id5]), frozenset([id1, id7]),
                          frozenset([id5, id7]), frozenset([id7, id4]),
                          frozenset([id3, id8]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8]),
                          frozenset([id1, id3]), frozenset([id2, id4]) 						  
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8]), frozenset([pid9, pid10]), frozenset([pid11, pid12])])  # noqa
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."

if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print ("Success!  All tests pass!")
