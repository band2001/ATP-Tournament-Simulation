import webbrowser, os.path
import random

def updateRanking(playerName, dic, lis):
    
    #built in function to update individual player ranking. Player name - any player name : dic == atp_data : lis == list of players
    
    oldRanking = dic[playerName][0]  #creates a value that is the players original ranking
    newRanking = 1
    for i in lis:   #for all 128 players in the atp rankings - i becomes the player names to be referenced in dic[i]
        if dic[playerName][1] < dic[i][1]: #this step compares the points of the player whose ranking is being updated to the other players on tour.
            newRanking += 1 #everytime someone has a higher number of points than the "playername," their ranking is increased (higher ranking number means lower ranked)
        else:
            continue #after this loop gives the player whose rank changed their new rank the rest of the code sorts the rest of the players.
    if newRanking == oldRanking: #if after the player's newRanking being calculated by the for loop above, if the oldRanking is the same as the new ranking then nothing happens
        dic[playerName][0] = newRanking
        return "Done"
    elif newRanking > oldRanking: #if the player's new ranking is greater than (meaning ranked lower) their previous ranking, it moves the players between oldRanking and newRanking up a spot (ranked higher a spot).
        for q in lis:
            for j in range(oldRanking, newRanking+1):
                if dic[q][0] == j:
                    dic[q][0] -= 1
                    break
                else:
                    continue
        dic[playerName][0] = newRanking
        del lis[oldRanking-1]
        lis.insert(newRanking-1,playerName)
        return "Done"
    elif oldRanking > newRanking:#if the player's new ranking is less than (meaning ranked higher) their previous ranking, it moves the players between newRanking and oldRanking down a spot (ranked lower a spot).
        for h in lis:
            for p in range(newRanking, oldRanking+1):
                if dic[h][0] == p:
                    dic[h][0] += 1
                    break
                else:
                    continue
        dic[playerName][0] = newRanking #Changes the dictionary (atp_data) to reflect the players new ranking
        del lis[oldRanking-1]              #These two lines rearrange players in atp_players list so that they are in the list in order of ranking. 
        lis.insert(newRanking-1,playerName)
        return "Done"

def matchUpdate(pointAmt,dic1,lis1):

    #gives user ability to input a single match and point value for the match. pointAmt -  number of points awarded : dic1(dicitonary containg player names, ranking, and points) - atp_data : lis1(list of player names with no other data) -- atp_players
    
    player1 = str(input("What is the name of the first player? Enter full ATP name with correct spacing and punctuation."))
    player2 = str(input("What is the name of the second player? Enter full ATP name with correct spacing and punctuation."))
    winner = input("Who won the match?")
    try:  #adds a set number of points (pointAmt) to the winning players atp data dictionary value.
        dic1[winner][1] += pointAmt
    except KeyError:
        print("One or more of the player names is not a valid ATP player in the top 128 rankings.")
        return None
    update = updateRanking(winner,dic1,lis1)   #update calls the previous function update ranking which sorts the dictionary values by points to determine the accurate world atp ranking.
    print("The match result has been recorded.")


def htmlRankings(dic1,lis1):

    #outputs the atp rankings data from the atp player data dictionary to a website. Needs dic1 the updated rankings dictionary and the list of players (lis1) to itterate through the dictionary.
    
    htmlRankings = '''<!DOCTYPE html>
    <html>
    <head>
        <title>ATP Rankings (1-128)</title> <!--Webpage title for tab-->
        <style>
            h1 {
                text-align: center;
                font-family: Garamond;
            }
            div.head {
                background-color: #808080;
                color: white;
                margin-top:4px;
            }
            div.primary {
                margin-left: auto;
                margin-right: auto;
                width: 50%;
                height: 25px;
            }
            div.gray {
                background-color: #778899;
            }
            span {
                display: inline-block;
                width: 33.33%;
                height: 25px;
                text-align: center;
                font-family: Helvetica;
                margin-top: 4px
            }
        </style>
    </head>
    <body>
        <!--Headings of Site and Table-->
        <h1>ATP Rankings (1-128)</h1>
        <div class="primary head"><span>Rank</span><span>Player</span><span>Points</span></div>
    '''
    for i in range(1,129):  #makes every other line of data a gray opposed to the white for an easier read
        if i % 2 == 0:
            htmlRankings += '''<div class="primary gray">'''
        else:
            htmlRankings += '''<div class="primary">'''
        for j in lis1: #since our dictionary keys are player names, for j in lis1; itterates through each player in the dictionary
            if dic1[j][0] == i: #adds the player name - rank(dic1[j][0])- and player points (dic1[j][1]) in order of ranking (dic1[j][0])
                htmlRankings += f'''<span>{dic1[j][0]}</span><span>{j}</span><span>{dic1[j][1]}</span></div>'''
                break
    htmlRankings += '''</body></html>'''

    output = open("ATP-Rankings.html","w")
    output.write(htmlRankings)
    output.close()

    webbrowser.open("file:///"+os.path.abspath("ATP-Rankings.html")) # Opens rankings in default browser

def getplayerdata(dic1):

    #calls current individual player data using player name.

    while True:
        try:
            player=input("Input Player Name:")
            dic1[player]
            rank=dic1[player][0] #calls dictionary value [0] which is rank
            atp_points=dic1[player][1] #calls dictionary value [1] which is points
            return(player,' is rank ',rank,'in the world with ',atp_points,'ATP Points') #output of player name, rank, and points
            break
        except KeyError: #error for invalid player names. Asks the user to try again.
            print("You have input a non-valid player name, please try again")

def editplayerdata(player,points_change,dic5,lis5):

    #way to manually edit player data without a match being played.
    
    while True:
        try:
            x=[]
            x=dic5[player]
            rank=x[0]
            points=x[1]
    
            dic5[player]=[rank,points+points_change] #Updates points in the atp_data dictionary

            updateRanking(player,dic5,lis5) #after the change in points, (updateRanking) is run for the player so the atp rankings list is updated
            return(dic5[player])
        except KeyError:
            print("You have input a non-valid player name, please try again")

def assignProbability(dic,lis): #assign probability breaks the top 128 players into 16 sub groups by ranking. This probability is later used to simulate matches, giving higher ranking players a higher chance of winning their simulated match 
    player_weight = {}
    for i in lis:
        if dic[i][0] <=8: #the top 8 players in the world recive the highest player weight
            player_weight[i] = 16
        elif dic[i][0] > 8 and dic[i][0] <= 16:
            player_weight[i] = 15
        elif dic[i][0] > 16 and dic[i][0] <= 24:
            player_weight[i] = 14
        elif dic[i][0] > 24 and dic[i][0] <= 32:
            player_weight[i] = 13
        elif dic[i][0] > 32 and dic[i][0] <= 40:
            player_weight[i] = 12
        elif dic[i][0] > 40 and dic[i][0] <= 48:
            player_weight[i] = 11
        elif dic[i][0] > 48 and dic[i][0] <= 56:
            player_weight[i] = 10
        elif dic[i][0] > 56 and dic[i][0] <= 64:
            player_weight[i] = 9
        elif dic[i][0] > 64 and dic[i][0] <= 72:
            player_weight[i] = 8
        elif dic[i][0] > 72 and dic[i][0] <= 80:
            player_weight[i] = 7
        elif dic[i][0] > 80 and dic[i][0] <= 88:
            player_weight[i] = 6
        elif dic[i][0] > 88 and dic[i][0] <= 96:
            player_weight[i] = 5
        elif dic[i][0] > 96 and dic[i][0] <= 104:
            player_weight[i] = 4
        elif dic[i][0] > 104 and dic[i][0] <= 112:
            player_weight[i] = 3
        elif dic[i][0] > 112 and dic[i][0] <= 120:
            player_weight[i] = 2
        elif dic[i][0] > 120 and dic[i][0] <= 128: #the system is such that if the highest ranked player in the world played the lowest ranked player in the world, there would be a 16/17 percent chance that the top seed would win (see user manual for more information).
            player_weight[i] = 1
    return player_weight

def tourneysim(dic2,lis2,points,dic3,lis3,dic4):

    #this function simulates a round of a grand slam. 
    
    nextround=[] #a blank list for players who win and move on to the next round
    htmlResults = [] #This is used to store strings with the results of the matches to be outputted to an HTML file once the tournament has been completed.
    iterate = int(len(lis2) / 2)  #iterate determines how many matches are played in the round.
    for i in range(iterate):
        score = random.random() #score is a random value between (0 and 1)
        player1=lis2.pop(0) #this takes the highest ranked player in lis2
        player2=lis2.pop(-1) #this takes the lowest ranked player in lis2
        player1prob=dic2[player1] #this calls the wieghted score created by the function assign probability
        player2prob=dic2[player2] #this calls the wieghted score created by the funciton assign probability
        rangeidentifier = (player1prob / (player1prob + player2prob))

        #This if/else statement determines the winner and then appends the winner to the nextround list.
        if 0 <= score <= rangeidentifier: #if player 1 wins the match
            nextround.append(player1) #Appends player 1 to the nextround list
            dic3[player1][1]+=points #adds a number of points to player 1's atp point total
            updateRanking(player1,dic3,lis3) #updates the player rankings
            if dic4[player1][0] <= 16 and dic4[player2][0] <= 16: #These sub if/else statements are used so that for the top 16 ranked players a (#) appears before their name with their ranking as #.
                htmlResults.append(f"({dic4[player1][0]}) {player1} , ({dic4[player2][0]}) {player2}")
            elif dic4[player1][0] <= 16:
                htmlResults.append(f"({dic4[player1][0]}) {player1} , {player2}")
            elif dic4[player2][0] <= 16:
                htmlResults.append(f"{player1} , ({dic4[player2][0]}) {player2}")
            else:
                htmlResults.append(f"{player1} , {player2}")

            
        else:
            nextround.append(player2) #if player 2 wins appends player 3 to the next round list.
            dic3[player2][1]+=points # adds a number of points to player 2's atp point total 
            updateRanking(player2,dic3,lis3) # updates the player rankings
            if dic4[player1][0] <= 16 and dic4[player2][0] <= 16: #These sub if/else statements are used so that for the top 16 ranked players a (#) appears before their name with their ranking as #.
                htmlResults.append(f"({dic4[player2][0]}) {player2} , ({dic4[player1][0]}) {player1}")
            elif dic4[player2][0] <= 16:
                htmlResults.append(f"({dic4[player2][0]}) {player2} , {player1}")
            elif dic4[player1][0] <= 16:
                htmlResults.append(f"{player2} , ({dic4[player1][0]}) {player1}")
            else:
                htmlResults.append(f"{player2} , {player1}")
    return nextround,htmlResults #the function returns a list of the players who won their match this round and the list of strings of results.

def roundWinners(dic1,lis1):

    #this function calls the previous function (tourneysiim) 7 times to simulate a full grand slam tournament.
    
    initRank = {}
    for j in lis1:
        initRank[j] = [dic1[j][0],dic1[j][1]]
    firstRound = lis1.copy()
    player_probabilities = assignProbability(dic1,lis1) #(assignProbability) calls the current atp tour data and runs creating a dictionary with players weighted odds of winning

    #In the following code, the first variable is the pure list of players returned from the tourneysim function, the second variable is the list that contains strings describing the results for later HTML output.

    secondRound,r1R = tourneysim(player_probabilities, firstRound,45,dic1,lis1,initRank) #this step simulates the first round of matches using player_probabilities and the atp rankings list. A point value of 45 is added to those who won their matches this round.
    thirdRound,r2R = tourneysim(player_probabilities, secondRound,90,dic1,lis1,initRank) #this step simulates the secondRound and assigns 90 tour points to the winners
    fourthRound,r3R = tourneysim(player_probabilities, thirdRound,180,dic1,lis1,initRank) #this step simulates the thirdRound and assigns 180 tour points to the winners
    quarterfinals,r4R = tourneysim(player_probabilities, fourthRound,360,dic1,lis1,initRank) #this step simulates the fourth round and assigns 360 points to the winners
    semifinals,qfR = tourneysim(player_probabilities, quarterfinals,720,dic1,lis1,initRank) #this step simulates the quater finals and assigns 720 points to the winners
    final,sfR = tourneysim(player_probabilities, semifinals,1200,dic1,lis1,initRank) #this step simulates the semifinals and assigns 1200 points to the winners
    champ,winner = tourneysim(player_probabilities,final,2000,dic1,lis1,initRank) #this step simulates the final match and outputs the tournoment winner
    printResultsHTML(r1R,r2R,r3R,r4R,qfR,sfR,winner) # Calls the function printResultsHTML to output the match results to a webpage using the string results lists.
        
def printResultsHTML(r128,r64,r32,r16,rQF,rSF,rF): # Outputs match results to an HTML file; requires a list of string results for each round.
    # Initial HTML Setup
    results = '''<!DOCTYPE html> 
    <html>
    <head>
        <title>Grand Slam Results</title>
        <style>
            h1 {
                text-align: center;
                font-family: Garamond;
            }
            h3 {
                text-align: center;
                font-family: Avenir;
            }
            p {
                font-family: Helvetica;
                text-align: center;
            }
            div.fr {
                width:25%;
                float:left;
            }
            div.tr {
                width:49%;
                float:left;
            }
        </style>
    </head>

    <body>
        <h1>Grand Slam Results</h1>
        <br>
    '''

    #There are seven different for loops below because each round has slightly different HTML formatting. The first two rounds for instance have four columns (4 divs are used) but have a different number of matches to output.
    q = 16
    results += "<h3>First Round Results</h3>"
    for i in range(4):
        results += "<div class='fr'>"
        for b in r128[q-16:q]:   #Takes the first 16 matchups to put in the first div, second 16 matchups for the second div, etc.
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:  #Used to make the top 16 seeds bold
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 16
        results += "</div>"
        
    results += "<h3>Second Round Results</h3>"

    #Similar process repeated for each div with slightly different formatting each time (that's why nested for loops weren't utilized).
    
    q = 8
    results += "<div>"
    for i in range(4):
        results += "<div class='fr'>"
        for b in r64[q-8:q]:
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 8
        results += "</div>"
    results += "</div>"
        
    
    results+= "<div><h3>Third Round Results</h3></div>"

    q = 8

    results += "<div>"

    for i in range(2):
        results += "<div class='tr'>"
        for b in r32[q-8:q]:
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 8
        results += "</div>"
        
    results += "</div>"
    results += "<h3>Round of 16 Results</h3>"

    q = 4

    results += "<div>"

    for i in range(2):
        results += "<div class='tr'>"
        for b in r16[q-4:q]:
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 4
        results += "</div>"

    results += "</div>"

    results += "<h3>Quarterfinal Results</h3>"

    q = 2

    results += "<div>"
    
    for i in range(2):
        results += "<div class='tr'>"
        for b in rQF[q-2:q]:
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 2
        results += "</div>"

    results += "</div>"
    results += "<h3>Semifinal Results</h3><div class='body'>"

    q = 1

    results += "<div>"
    
    for i in range(2):
        results += "<div class='tr'>"
        for b in rSF[q-1:q]:
            people = b.split(",")
            if "(" in people[0] and "(" in people[1]:
                results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
            elif "(" in people[0]:
                results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
            elif "(" in people[1]:
                results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
            else:
                results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
        q += 1
        results += "</div>"

    results += "</div>"

    results += "<h3>Championship Result</h3>"

    results += "<div>"

    for b in rF:
        people = b.split(",")
        if "(" in people[0] and "(" in people[1]:
            results += f'''<p><b>{people[0]}</b> defeated <b>{people[1]}</b></p><br>'''
        elif "(" in people[0]:
            results += f'''<p><b>{people[0]}</b> defeated {people[1]}</p><br>'''
        elif "(" in people[1]:
            results += f'''<p>{people[0]} defeated <b>{people[1]}</b></p><br>'''
        else:
            results += f'''<p>{people[0]} defeated {people[1]}</p><br>'''
    
    
    results += '''</div></body></html>'''
    
    output = open("GS-Results.html","w")  #Writes the results to an HTML file
    output.write(results)
    output.close()

    webbrowser.open("file:///"+os.path.abspath("GS-Results.html"))  #Opens the HTML file in a browser 

