import functions
import random
import copy

#This part of code opens the CSV file with the player data and extracts the information to a dictonary and list.

atp = open("atp_player_data.csv","r")

atp_data = {} #A dictionary with player names as keys and lists with [player's ranking,player's points] as values.
atp_players = [] #A list of players in order of their rankings (1st ranked is first, 128th last)

for line in atp:
  data = line.split(",")
  if data[0] == "Ranking":
    continue
  atp_players.append(data[1])
  atp_data[data[1]] = [int(data[0]),int(data[3])]

atp.close()

#Data is now in the atp_data dictionary and atp_player list.

originalatp_data=copy.deepcopy(atp_data) #Makes a copy of atp_data so user can reset the atp_data after it is modified in simulations.
originalatp_players=copy.deepcopy(atp_players)

#All of the following functions call functions from functions.py.
#The purpose of having these functions is they don't make the user input the atp_data dictionary and atp_player list.
#In other words, this minimizes user error from people that aren't familiar with the parameters of the funtions in functions.py.

def matchResult(points=10): #Allows a user to manually input a match between two players to adjust their ranking. Users can enter an integer as a parameter to specify how many points they want the match have; default is 10
  functions.matchUpdate(points,atp_data,atp_players) #Calls matchUpdate function from functions.py with parameters already filled out.

def printRankings(): #Opens an HTML file of rankings in default browser; calls htmlRankings from functions.py
  functions.htmlRankings(atp_data,atp_players)

def getPlayerData(): #Gets an individual player's data
  functions.getplayerdata(atp_data)

def editPlayerData(): #Can manually edit a playerr's points without simulating a match or tournament.
  player = input("What player would you like to edit?")
  points_change = int(input("How would you like their points to change?"))
  atp_data[player] = functions.editplayerdata(player,points_change,atp_data,atp_players)
  functions.updateRanking(player,atp_data,atp_players)

def simulateTournament(): #Simulates a Grand Slam Tournament
  functions.roundWinners(atp_data,atp_players)






