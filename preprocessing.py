import pandas as pd
import numpy as np
import statistics as stats
from statistics import mode, StatisticsError

#load data and create features dataset and class dataset


global output



def getPlayerData():
    global output
    dataframe = pd.read_csv("specialData/player_attributes.csv",keep_default_na=False)
    playerDataList = list()
    playerID=-1
    columnsNames= ['player_fifa_api_id','player_api_id','date',	'overall_rating',	'potential',	'preferred_foot',	'attacking_work_rate',	'defensive_work_rate',	'crossing',	'finishing',	'heading_accuracy',	'short_passing',	'volleys',	'dribbling',	'curve',	'free_kick_accuracy',	'long_passing',	'ball_control',	'acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'shot_power',	'jumping',	'stamina',	'strength',	'long_shots',	'aggression',	'interceptions',	'positioning',	'vision',	'penalties',	'marking',	'standing_tackle',	'sliding_tackle',	'gk_diving',	'gk_handling',	'gk_kicking',	'gk_positioning',	'gk_reflexes']
    output = pd.DataFrame(columns= columnsNames)
    for  index, row in dataframe.iterrows():
        id = row['player_api_id']
        if (len(playerDataList)==0):
            playerDataList.append(row)
            playerID=id
        elif (id==playerID):
           playerDataList.append(row)
        elif (len(playerDataList) > 0) :
            splitPlayerDataByYear(playerDataList)
            playerDataList.clear()
            playerDataList.append(row)
            playerID = id
    splitPlayerDataByYear(playerDataList)
    output.to_csv("specialData/average_player_attributes.csv")


def splitPlayerDataByYear(playerDataList) :
    playerDataByYear = list()
    dataYear=0
    for row in playerDataList :
        date = row['date']
        year=""
        if (date!=""):
            splitDate = date.split("/")
            yeartemp = splitDate[2]
            yearArr = yeartemp.split(" ")
            year = yearArr[0]
        if(len(playerDataByYear)==0):
            dataYear=year
            playerDataByYear.append(row)
        elif(year==dataYear):
            playerDataByYear.append(row)
        else:
            calculatePlayerAverageByYear(playerDataByYear)
            playerDataByYear.clear()
            playerDataByYear.append(row)
            dataYear = year
    calculatePlayerAverageByYear(playerDataByYear)

def calculatePlayerAverageByYear(playerYearData):
    global output
    if (len(playerYearData) > 0):
        playerAttributeDic = dict()
        for featureName in playerYearData[0].keys():
            playerAttributeDic[featureName]=list()
        playerAttributeDic["player_fifa_api_id"].append(playerYearData[0]['player_fifa_api_id'])
        playerAttributeDic["player_api_id"].append(playerYearData[0]['player_api_id'])
        date = playerYearData[0]['date']
        splitDate = date.split("/")
        yeartemp = splitDate[2]
        yearArr = yeartemp.split(" ")
        year = yearArr[0]
        playerAttributeDic["date"].append(year)
        playerAttributeDic["preferred_foot"].append(playerYearData[0]['preferred_foot'])
        for row in playerYearData:
            playerAttributeDic["attacking_work_rate"].append(row['attacking_work_rate'])
            playerAttributeDic["defensive_work_rate"].append(row['attacking_work_rate'])
            playerAttributeDic["penalties"].append(row['penalties'])
            playerAttributeDic["overall_rating"].append(row['overall_rating'])
            playerAttributeDic["potential"].append(row['potential'])
            playerAttributeDic["crossing"].append(row['crossing'])
            playerAttributeDic["finishing"].append(row['finishing'])
            playerAttributeDic["heading_accuracy"].append(row['heading_accuracy'])
            playerAttributeDic["short_passing"].append(row['short_passing'])
            playerAttributeDic["volleys"].append(row['volleys'])
            playerAttributeDic["dribbling"].append(row['dribbling'])
            playerAttributeDic["curve"].append(row['curve'])
            playerAttributeDic["free_kick_accuracy"].append(row['free_kick_accuracy'])
            playerAttributeDic["long_passing"].append(row['long_passing'])
            playerAttributeDic["ball_control"].append(row['ball_control'])
            playerAttributeDic["acceleration"].append(row['acceleration'])
            playerAttributeDic["sprint_speed"].append(row['sprint_speed'])
            playerAttributeDic["agility"].append(row['agility'])
            playerAttributeDic["reactions"].append(row['reactions'])
            playerAttributeDic["balance"].append(row['balance'])
            playerAttributeDic["shot_power"].append(row['shot_power'])
            playerAttributeDic["jumping"].append(row['jumping'])
            playerAttributeDic["stamina"].append(row['stamina'])
            playerAttributeDic["strength"].append(row['strength'])
            playerAttributeDic["long_shots"].append(row['long_shots'])
            playerAttributeDic["aggression"].append(row['aggression'])
            playerAttributeDic["interceptions"].append(row['interceptions'])
            playerAttributeDic["positioning"].append(row['positioning'])
            playerAttributeDic["vision"].append(row['vision'])
            playerAttributeDic["marking"].append(row['marking'])
            playerAttributeDic["standing_tackle"].append(row['standing_tackle'])
            playerAttributeDic["sliding_tackle"].append(row['sliding_tackle'])
            playerAttributeDic["gk_diving"].append(row['gk_diving'])
            playerAttributeDic["gk_handling"].append(row['gk_handling'])
            playerAttributeDic["gk_kicking"].append(row['gk_kicking'])
            playerAttributeDic["gk_positioning"].append(row['gk_positioning'])
            playerAttributeDic["gk_reflexes"].append(row['gk_reflexes'])
        playerAverageDic = calaculateAverage(playerAttributeDic)
        output = output.append(playerAverageDic, ignore_index=True)


def calaculateAverage(playerAttributeDic):
    playerAverageDic = dict()
    for key in playerAttributeDic.keys():
        values = playerAttributeDic[key]
        if(len(values)==1):
            playerAverageDic[key]=values[0]
        elif(len(values)>1):
            if(key == "attacking_work_rate" or key == "defensive_work_rate"):
                try:
                    playerAverageDic[key] = stats.mode(values)
                except StatisticsError:
                    if(values[0]!=""):
                        playerAverageDic[key] = values[0]
                    else:
                        playerAverageDic[key]=""
            else:
                counter=0
                sum=0
                for value in values:
                    average=""
                    if(value!=""):
                        counter = counter+1
                        sum = sum + int(value)
                if(counter>0):
                    average=sum/counter
                playerAverageDic[key]=average
    return playerAverageDic
def missinData():
    df = pd.read_csv('newData/testMatchSplitTeam.csv')
    col = ['home_win', 'home_draw','home_lose','away_win','away_draw','away_lose' ]


    for c  in col:
        df[c].fillna(df[c].mean(), inplace=True)
    df.to_csv('test5.csv',header=True )



missinData()
# getPlayerData()

