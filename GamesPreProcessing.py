import pandas as pd
import numpy as np
import statistics as stats

global players_Dictionary
global playersAttributes
global diffanceAttributes
global attackingAttributes
global goalkepperAttributes
global commonAttributes
global matchesNotSpliting
global matchAttributes

def loadAttributes():
    global players_Dictionary
    global playersAttributes
    global diffanceAttributes
    global attackingAttributes
    global goalkepperAttributes
    global commonAttributes
    global matchAttributes
    playersAttributes = ['overall_rating',	'potential'	,'crossing'	,'finishing','penalties','free_kick_accuracy','heading_accuracy',	'short_passing',	'volleys'	,'dribbling',	'curve'	,'free_kick_accuracy',	'long_passing'	,'ball_control',	'acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'shot_power',	'jumping',	'stamina',	'strength',	'long_shots',	'aggression',	'interceptions',	'positioning',	'vision',	'penalties',	'marking',	'standing_tackle',	'sliding_tackle',	'gk_diving',	'gk_handling',	'gk_kicking',	'gk_positioning',	'gk_reflexes']
    goalkepperAttributes = ['gk_diving','gk_handling',	'gk_kicking',	'gk_positioning',	'gk_reflexes']
    attackingAttributes = ['finishing','shot_power','long_shots','vision','volleys','dribbling','curve']
    diffanceAttributes = ['balance',	'strength',	'standing_tackle',	'sliding_tackle']
    commonAttributes = ['overall_rating','potential','crossing','heading_accuracy','short_passing', 'long_passing'	,'ball_control','acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'jumping',	'stamina',	'strength',	'aggression',	'interceptions',	'positioning',	'marking']
    matchAttributes = ['season','stage','match_api_id','home_team_api_id','away_team_api_id','home_ratio','draw_ratio','away_ratio','result','overall_rating',	'potential'	,'crossing'	,'finishing',	'heading_accuracy',	'short_passing',	'volleys'	,'dribbling',	'curve'	,'free_kick_accuracy',	'long_passing'	,'ball_control',	'acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'shot_power',	'jumping',	'stamina',	'strength',	'long_shots',	'aggression',	'interceptions',	'positioning',	'vision',	'penalties',	'marking',	'standing_tackle',	'sliding_tackle',	'gk_diving',	'gk_handling',	'gk_kicking',	'gk_positioning',	'gk_reflexes']


def getPlayersByTeam(gameTeam, row):
    players = list()
    for x in range(1, 12):
        player=row[gameTeam+ str (x)]
        players.append(player)
    return players

def getPlayersData(players,yearSt):
    global players_Dictionary
    year=0
    if(yearSt!=""):
        year=int(yearSt)-1
    else:
        year=2007
    playersData =list()
    for id in players:
        if(id!="" and int (id) in players_Dictionary):
            playerData=players_Dictionary[int(id)]
            playerYearData=getPlayerByYear(playerData,year)
            if(isinstance(playerYearData, str)==False):
                playersData.append(playerYearData)
            else:
                playersData.append("")
        else:
            playersData.append("")
    return playersData

def loadPlayersData():
    dataframe = pd.read_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\average_player_attributes.csv",keep_default_na=False)
    global players_Dictionary
    players_Dictionary =dict()
    playerYearList=list()
    playerID=0
    for  index, row in dataframe.iterrows():
        id = row['player_api_id']
        if(len(playerYearList)==0):
            playerID=id
            playerYearList.append(row)
        elif(playerID==id):
            playerYearList.append(row)
        else:
            players_Dictionary[playerID]=playerYearList
            playerYearList = list()
            playerYearList.append(row)
            playerID = id
    players_Dictionary[playerID] = playerYearList



def getPlayerByYear(playerData,year):
    for season in playerData:
        dateS=season['date']
        date= int (dateS)
        if(date==year):
            return season
    lastReleventYear=""
    releventyear=0
    for season in playerData:
        dateS = season['date']
        date = int(dateS)
        if (date < year):
            if(date > releventyear):
                lastReleventYear=season
                releventyear=date
    return lastReleventYear

def calculateTeamAttributes(players,attributeList):
    attributeCounterDict=dict()
    attributeSumDict= dict()
    attributeAverageDict=dict()
    for attribute in attributeList :
        attributeCounterDict[attribute]=0
        attributeSumDict[attribute]=0
        attributeAverageDict[attribute]=0
    for player in players :
        if(isinstance(player, str)==False):
            for attribute in player.keys():
                if(attributeList.count(attribute)>0):
                    attributeCounterDict[attribute]+=1
                    attributeSumDict[attribute] += float (player[attribute])
    for attribute in attributeSumDict.keys():
        sum = attributeSumDict[attribute]
        counter =  attributeCounterDict[attribute]
        if(counter>0):
            average = sum/counter
        else:
            average = 0
        attributeAverageDict[attribute] = average
    return attributeAverageDict

def getMachesDataByAllTeam():
    global matchesNotSpliting
    global matchAttributes
    loadAttributes()
    matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
    dataframe = pd.read_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\trainingDataNoMissingPlayers.csv",keep_default_na=False)
    loadPlayersData()
    counter=0
    flag=True
    for  index, match in dataframe.iterrows():
        gameDic=dict()
        gameDic['season'] = match['season']
        gameDic['stage'] = match['stage']
        gameDic['match_api_id'] = match['match_api_id']
        gameDic['home_team_api_id'] = match['home_team_api_id']
        gameDic['away_team_api_id'] = match['away_team_api_id']
        gameDic['result']=getResult(match['home_team_goal'],match['away_team_goal'])
        ratios=calculateGamblingRatio(match)
        gameDic['home_ratio'] = ratios[0]
        gameDic['draw_ratio'] = ratios[1]
        gameDic['away_ratio'] = ratios[2]
        homePlayers = getPlayersByTeam("home_player_", match)
        awayPlayers = getPlayersByTeam("away_player_", match)
        season=match['season']
        year=season.split("/")[0]
        awayPlayersData = getPlayersData(awayPlayers,year)
        homePlayersData = getPlayersData(homePlayers,year)
        awayPlayerAverage = createTeamAttributesByNotSpliting (awayPlayersData)
        homePlayerAverage = createTeamAttributesByNotSpliting (homePlayersData)
        mergeDic = teamDiffrencesAttributes (homePlayerAverage,awayPlayerAverage)
        fullGame={**mergeDic, **gameDic}
        if(counter>2000):
            if(flag):
                matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingNoSplit.csv")
                matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
                counter=0
                flag=False
                print("2000")
            else:
                matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingNoSplit.csv", header=False, mode='a')
                matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
                counter=0
                print("2000")
        else:
            counter+=1
            matchesNotSpliting = matchesNotSpliting.append(fullGame, ignore_index=True)
    matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingNoSplit.csv", header=False, mode='a')


def getMachesDataBysplitTeam():
    global matchesNotSpliting
    global matchAttributes
    loadAttributes()
    matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
    dataframe = pd.read_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\trainingDataNoMissingPlayers.csv",keep_default_na=False)
    loadPlayersData()
    counter=0
    flag=True
    for  index, match in dataframe.iterrows():
        gameDic=dict()
        gameDic['season'] = match['season']
        gameDic['stage'] = match['stage']
        gameDic['match_api_id'] = match['match_api_id']
        gameDic['home_team_api_id'] = match['home_team_api_id']
        gameDic['away_team_api_id'] = match['away_team_api_id']
        gameDic['result']=getResult(match['home_team_goal'],match['away_team_goal'])
        ratios=calculateGamblingRatio(match)
        gameDic['home_ratio'] = ratios[0]
        gameDic['draw_ratio'] = ratios[1]
        gameDic['away_ratio'] = ratios[2]
        homePlayers = getPlayersByTeam("home_player_", match)
        awayPlayers = getPlayersByTeam("away_player_", match)
        season=match['season']
        year=season.split("/")[0]
        awayPlayersData = getPlayersData(awayPlayers,year)
        homePlayersData = getPlayersData(homePlayers,year)
        awayPlayerAverage = createTeamAttributesBySplitTeam (awayPlayersData)
        homePlayerAverage = createTeamAttributesBySplitTeam (homePlayersData)
        mergeDic = teamDiffrencesAttributes (homePlayerAverage,awayPlayerAverage)
        fullGame={**mergeDic, **gameDic}
        if(counter>2000):
            if(flag):
                matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingSplitTeam.csv")
                matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
                counter=0
                flag=False
                print("write2000")
            else:
                matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingSplitTeam.csv", header=False, mode='a')
                matchesNotSpliting = pd.DataFrame(columns=matchAttributes)
                counter=0
                print("write2000")
        else:
            counter+=1
            matchesNotSpliting = matchesNotSpliting.append(fullGame, ignore_index=True)
    matchesNotSpliting.to_csv(r"C:\Users\gal\Desktop\ISE\semesterF\project\data\\matchTrainingSplitTeam.csv", header=False, mode='a')


def teamDiffrencesAttributes (home,away):
    diffrenceDic=dict()
    for attribute in home.keys():
        diffrence = (home[attribute] - away[attribute])/100
        diffrenceDic[attribute]=diffrence
    return diffrenceDic


def calculateGamblingRatio(match):
    homeRatio=0
    drawRatio=0
    awayRatio=0
    homeList = ['B365H','BWH','IWH','LBH','WHH',' SJH','VCH','PSH','BSH']
    drawList = ['B365D','BWD','IWD','LBD','WHD',' SJD','VCD','PSD','BSD']
    awayList = ['B365A','BWA','IWA','LBA','WHA',' SJA','VCA','PSA','BSA']
    for col in match.keys():
        if(homeList.count(col)>0):
            homeRatio += float(match[col])
        elif(drawList.count(col)>0):
            drawRatio +=float(match[col])
        elif(awayList.count(col)>0):
            awayRatio+=float(match[col])
    if(homeRatio==0 or drawRatio==0 or awayRatio==0 ):
        results = [0, 0, 0]
        return results
    home=7/homeRatio
    draw=7/drawRatio
    away=7/awayRatio
    results=[home,draw,away]
    return results


def getResult(homeGoal, awayGoal):
    hScore = int(homeGoal)
    awayScore= int (awayGoal)
    if(hScore>awayScore):
        return 1
    if(hScore<awayScore):
        return -1
    return 0

def createTeamAttributesByNotSpliting(playersData):
    global playersAttributes
    playerAverageAttribute = calculateTeamAttributes (playersData,playersAttributes)
    return playerAverageAttribute

def getMostValuePenalties(playersData):
    penalties = 0
    for player in playersData:
        if(isinstance(player, str)==False):
            playerPenaltie = float(player['penalties'])
            if (playerPenaltie > penalties):
                penalties = playerPenaltie
    return penalties

def getMostValuefreeKick(playersData):
    free_kick_accuracy = 0
    for player in playersData:
        if (isinstance(player, str) == False):
            playerFreeKick = float(player['free_kick_accuracy'])
            if (playerFreeKick > free_kick_accuracy):
                free_kick_accuracy = playerFreeKick
    return free_kick_accuracy

def createTeamAttributesBySplitTeam(playersData):
    global diffanceAttributes
    global attackingAttributes
    global goalkepperAttributes
    global commonAttributes
    goalKeppers=list()
    attackingPlayers=list()
    defensePlayers=list()
    for player in range(0,11):
        if(player==0):
            goalKeppers.append(playersData[player])
        elif(player<6):
            defensePlayers.append(playersData[player])
        else:
            attackingPlayers.append(playersData[player])
    goalKepperAttributes = calculateTeamAttributes (goalKeppers,goalkepperAttributes)
    defenceAttributes = calculateTeamAttributes (defensePlayers,diffanceAttributes)
    attackingAttributes1 = calculateTeamAttributes (attackingPlayers,attackingAttributes)
    coomanAttributes = calculateTeamAttributes (playersData,commonAttributes)
    fullgame={**goalKepperAttributes,**defenceAttributes,**attackingAttributes1, **coomanAttributes}
    fullgame['penalties'] = getMostValuePenalties(playersData)
    fullgame['free_kick_accuracy'] = getMostValuefreeKick(playersData)
    return fullgame

getMachesDataBysplitTeam()
getMachesDataByAllTeam()