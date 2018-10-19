# Noah Purcell
# Analysis of age of peak performance of hitters
# Mine the data for the age of peak output of hr, obp, slg
    
def getPeakAges(df, stat):
    grouped = df.groupby("playerID")
    peakAges = list()
    
    for plyrID, plyrStats in grouped:
        maxStat = plyrStats[stat].aggregate(max)
        pkAge = plyrStats[plyrStats[stat] == maxStat]["Age"]
        try:  # this will work when we have one peak age
            pkAge = int(pkAge)
            if stat == "OBP":
                traded_pk_age = check_traded_years_OBP(plyrStats, maxStat, pkAge)
            elif stat == "SLG":
                traded_pk_age = check_traded_years_SLG(plyrStats, maxStat, pkAge)
            elif stat == "HR":
                traded_pk_age = check_traded_years_HR(plyrStats, maxStat, pkAge)
            if traded_pk_age is not None:
                pkAge = traded_pk_age
            peakAges.append(pkAge)
        except TypeError: # in the case of a tie we'll count both peak ages
            multiplePks = list(plyrStats[plyrStats[stat] == maxStat]["Age"].astype(int))
            peakAges += multiplePks
    return peakAges

def check_traded_years_OBP(plyrStats, maxOBP, pkAge):
    if plyrStats["stint"].isin([2]).mean() != 0:
        tradedYears = plyrStats[plyrStats["stint"] == 2]["yearID"].values
        for year in tradedYears:
            totalH = plyrStats[plyrStats["yearID"] == year]["H"].sum()
            totalBB = plyrStats[plyrStats["yearID"] == year]["BB"].sum()
            totalHBP = plyrStats[plyrStats["yearID"] == year]["HBP"].sum()
            totalAB = plyrStats[plyrStats["yearID"] == year]["AB"].sum()
            totalSF = plyrStats[plyrStats["yearID"] == year]["SF"].sum()
            tradedYearOBP = (totalH + totalBB + totalHBP) / (totalAB + 
                            totalBB + totalHBP + totalSF)
            if tradedYearOBP > maxOBP:
                maxOBP = tradedYearOBP
                pkAge = int(plyrStats[plyrStats["yearID"] == year]["Age"])
                print("best year was traded year")
                print(plyrStats)
                return pkAge
    return None


def check_traded_years_SLG(plyrStats, maxSLG, pkAge):
    if plyrStats["stint"].isin([2]).mean() != 0:
        tradedYears = plyrStats[plyrStats["stint"] == 2]["yearID"].values
        for year in tradedYears:
            totalAB = plyrStats[plyrStats["yearID"] == year]["AB"].sum()
            total1B = plyrStats[plyrStats["yearID"] == year]["1B"].sum()
            total2B = plyrStats[plyrStats["yearID"] == year]["2B"].sum()
            total3B = plyrStats[plyrStats["yearID"] == year]["3B"].sum()
            totalHR = plyrStats[plyrStats["yearID"] == year]["HR"].sum()
            tradedYearSLG = (total1B + 2*(total2B) + 3*(total3B) + 4*(totalHR)) / (totalAB)
            if tradedYearSLG > maxSLG:
                maxSLG = tradedYearSLG
                pkAge = int(plyrStats[plyrStats["yearID"] == year]["Age"])
                print("best year was traded year")
                print(plyrStats)
                return pkAge
    return None

def check_traded_years_HR(plyrStats, maxHR, pkAge):
    if plyrStats["stint"].isin([2]).mean() != 0:
        tradedYears = plyrStats[plyrStats["stint"] == 2]["yearID"].values
        for year in tradedYears:
            tradedYearHR = plyrStats[plyrStats["yearID"] == year]["HR"].sum()
            if tradedYearHR > maxHR:
                maxHR = tradedYearHR
                pkAge = int(plyrStats[plyrStats["yearID"] == year]["Age"])
                print("best year was traded year")
                print(plyrStats)
                return pkAge
    return None
