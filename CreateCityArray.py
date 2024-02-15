import pandas as pd
cityData = pd.read_csv("cities.csv")
currentCities = []

def Create(inputnum):
    Cities5000 = cityData.iloc[:inputnum] #5000
    global cityX,cityY
    cityX = Cities5000['X']
    cityY = Cities5000['Y'] 
    populateMap()
    return currentCities[:]


def populateMap():
    for i in range(0,5000):#500
        #currentCities.append(((random.randrange(0,5000)),(random.randrange(0,5000))))
        currentCities.append((cityX[i],cityY[i]))

