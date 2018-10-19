# Noah Purcell
# Analysis of age of peak performance of hitters
# read in Batting data from Lahman database 
# filters data from source to prepare for peakAge study

import pandas as pd
import numpy as np

def load_data():
    batting = pd.read_csv("Batting.csv")
    master = pd.read_csv("Master.csv")
    
    # we only need birthYear from master
    birthYears = master.iloc[:,:2]
    batting["yearID"] = batting["yearID"].astype(int)
    ltrThan60 = batting["yearID"] >= 1955
    rows = ["playerID", "yearID", "stint", "teamID", "AB", "R", "H", "2B", "3B", "HR", "BB", "IBB", "HBP", "SF"]
    batting = batting[ltrThan60]
    batting = batting[rows]
    batting = batting.merge(birthYears, on="playerID")
    # Calculate age
    batting["Age"] = batting["yearID"] - batting["birthYear"]
    
    global enoughABsLst
    enoughABsLst = enoughABs(batting)
    batting["EnoughABs"] = batting["playerID"].apply(haveEnoughCareerABs)
    
    batting = batting[batting["EnoughABs"] == True]
    
    batting["OBP"] = (batting["H"] + batting["BB"] + batting["HBP"]) / (batting["AB"] + batting["BB"]
    + batting["HBP"] + batting["SF"])
    batting["1B"] = (batting["H"] - batting["2B"] - batting["3B"] - batting["HR"])
    batting["SLG"] = (batting["1B"] + (2 * batting["2B"]) + (3 * batting["3B"]) + (4 * batting["HR"]))/ batting["AB"]
    batting["OPS"] = batting["OBP"] + batting["SLG"]
    
    batting = haveEnoughSeasonABs(batting)
    
    return batting
    
def enoughABs(data):
    atBats = data[["playerID", "AB"]]
    atBatGroup = atBats.groupby(["playerID"]).sum()
    
    lst = []
    for index, row in atBatGroup.iterrows():
        if row["AB"] >= 1500:
            lst.append(index)
            
    return lst

def haveEnoughCareerABs(player):
    if player in enoughABsLst:
        return True
    return False

def seasonAb130(row):
    playerSeason = grouped.get_group((row["playerID"], row["yearID"]))
    seasonAb = playerSeason.aggregate(np.sum)["AB"]
    if seasonAb >= 130:
        return True
    return False

def haveEnoughSeasonABs(data):    
    global grouped
    grouped = data.groupby(["playerID", "yearID"])

    data["SeasonAB"] = data.apply(seasonAb130, axis=1)
    data = data[data["SeasonAB"] == True]

    return data
    
    