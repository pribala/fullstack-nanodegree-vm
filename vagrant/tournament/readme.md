# Tournament Results Project

This project consists of a Python module that uses the PostgreSQL database to keep track of players and matches 
in a game tournament.

The game tournament uses the Swiss system for pairing up players in each round: 
players are not eliminated, and each player is paired with another player with the same number of wins, 
or as close as possible.

### Installation

Clone this repository using:

git clone https://github.com/pribala/fullstack-nanodegree-vm.git

### Using the Vagrant Virtual Machine

This project is done within the Vagrant virtual machine.The Vagrant VM has PostgreSQL installed and configured, 
as well as the psql command line interface (CLI), so that you don't have to install or configure them on your 
local machine.
To use the Vagrant virtual machine, navigate to the ~/fullstack-nanodegree-vm/vagrant/ directory in the 
terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh 
(logs into the virtual machine).
Once you have executed the vagrant ssh command, you will want to cd /vagrant to change directory to the synced 
folders in order to test the project.
You'll need to have your VM on and be logged into it to run your database configuration file (tournament.sql), 
and test your Python file with tournament_test.py.

### Using the tournament.sql file

The tournament.sql file should be used for setting up your schema and database prior to use of the 
database for reporting and managing tournament players and matches. This file needs to be run only once.
The sql file contains all the sql commands needed to create the database, tables, and views. The purpose of this 
file is to set up the data structure: the tables and views. 
To build and access the database we run psql followed by \i tournament.sql

### Using the tournament_test.py

The test program verifies that the below functions are working properly.

deleteMatches()

Deletes all matches from a tournament to restart the tournament with the same players.

deletePlayers()

Delete all players to start with new players.

registerPlayer(name)

Register a new player in the tournament.

countPlayers()

Count the number of players in the tournament.

playerStandings()

Get the player standings.

reportMatch(winner, loser)

Update the tournament results by reporting the winner and loser of a match.

swissPairings()

Get the pairings for the next matches.

### What's Included

Within the repo you'll find the following directories and files:

  * /vagrant/tournament 
      * tournament.sql - this file is used to set up your database schema (the table representation of your data structure).
      * tournament.py -  this file is used to provide access to your database via a library of functions which can add, 
	                     delete or query data in your database to another python program (a client program)
      * tournament_test.py -  this is a client program which will use your functions written in the tournament.py module.
      * tournament_script.py - this script file can be used to generate random matches 

### Command line instructions to setup the database and run tests on the module:

Navigate to /vagrant/tournament (after the VM is running and you are logged in). Then run the following commands

$psql -f tournament.sql : runs the tournament.sql file to build and access the tournament database

$python tournament_test.py : runs the test functions for the module. 

### Reference:
  * Udacity's Intro to Relational Databases course
  * PostgreSQL Documentation
  * psycopg2 documentation
  * The webcasts for the Tournament Results Project
  
  