import math
import random
from threading import Thread
from multiprocessing import Pool
import datetime;
import CreateCityArray;


currentCities = []
iterations = 2000
startTemperature = 5000
currentTemperature = startTemperature
tasks = []

bestRouteQ1 = []
bestRouteQ2 = []
bestRouteQ3 = []
bestRouteQ4 = []


bestScore = float('inf')
bestRoute = []

def main():    
    global currentTemperature, currentCities, bestScore , bestRoute, Cities5000, cityX, cityY , bestRouteQ1,bestRouteQ2 ,bestRouteQ3,bestRouteQ4
    
    print("Time Started: {}".format(datetime.datetime.now()))        
    currentCities = CreateCityArray.Create(int(input("How Many cities?")))
    print("Working...")
    objectiveFunction(currentCities)
    bestRoute = iterate(currentCities, currentTemperature)    
    #Devides Array up
    number=len(currentCities)
    number = int((number * 0.25)//1)
    for i in range(0,number): #(0,1249)
        bestRouteQ1.append(bestRoute[i])        
    for i in range(number,number*2): #(1249,1499)
        bestRouteQ2.append(bestRoute[i])
    for i in range(number*2,number*3): #(1499,3748)
        bestRouteQ3.append(bestRoute[i])
    for i in range(number*3,len(currentCities)): #(3748,4997)
        bestRouteQ4.append(bestRoute[i])


def iterate(Cities, cTemp):  
    Score= bestScore 
    Route = bestRoute
    
    for i in range (0,iterations):
        newCities = citySwap(Cities)
        newObjectiveScore = objectiveFunction(newCities)
        currentObjectiveScore = objectiveFunction(Cities)
        
        if currentObjectiveScore < Score:
            Score = currentObjectiveScore            
            Route = newCities                

        if (makeSwap(currentObjectiveScore, newObjectiveScore, cTemp)):
            Cities = newCities

        cTemp = cTemp/(i+1)

        if i % 100 == 0:
          print("Iteration {}, Best Score: {}".format(i, routecalc(Route)))
          
    print("Best Score " , routecalc(Route))
    return Route


#Decides if swap should be made
def makeSwap(originalScore, newScore, temperature):
    randomChance = random.randint(0,startTemperature)
    swap = True
    if originalScore < newScore:
        swap = False
        if randomChance < temperature:
            swap = True
    if originalScore> newScore:
        swap = True
        if randomChance < temperature:
            swap = False
    
    return swap

#Swaps cities
def citySwap(cityList):
    newCityList = list(cityList)
    cityA = random.randrange(0,len(cityList))
    cityB = random.randrange(0,len(cityList))        
    newCityList[cityA], newCityList[cityB] = cityList[cityB], cityList[cityA]   

    return newCityList


#Finds Cities "Score" of each city
def objectiveFunction(cityList):
    cumulativeDistance = euclidianDistance(cityList[0], cityList[-1])

    for i in range(0, len(cityList)- 1):
        cumulativeDistance = cumulativeDistance + euclidianDistance(cityList[i],cityList[i+1])
    return cumulativeDistance

#Finds Distance between Cities
def euclidianDistance(city1,City2):
    return (city1[0] - City2[0])**2 + (city1[1] - City2[1])**2

def FinalDistanceCalc(city1,City2):
    number =  math.sqrt((city1[0] - City2[0])**2 + (city1[1] - City2[1])**2)
    return number


def routecalc(route):
    dist = 0.0
    for i in range(0, len(route)):
        next = (i+1)%len(route)
        dist += FinalDistanceCalc(route[i],route[next])
    return dist


def argGroup(args):
    return twoOpt1(*args)
    

def twoOpt1(route,TaskName):
    best = route
    improved = True
    for i in range(0,100):
        print(TaskName)
        improved = False
        print("TwoOpt{}".format(TaskName))   
        for i in range(0, len(route)-1):      
            for j in range(i + 1, len(route)):       
                if j - i == 1: 
                    continue
                         
                new_route = route[:]                        
                new_route[i:j] = route[j - 1:i - 1:-1]  # Reverse the segment between i and j
                #comapares the new order to the old order
                improveDist = CompareDist(route,new_route,i,j)
                # if there is an improvement then...
                if improveDist < 0:                   
                    best = new_route
                    improved = True
                    print("Improved {}".format(TaskName))
                    break        
    return best 

def CompareDist(route,newroute,i,j):
    oldDist = (euclidianDistance(route[i-1],route[i]) + euclidianDistance(route[j-1],route[j]))
    newDist = (euclidianDistance(newroute[i-1],newroute[j-1]) + euclidianDistance(newroute[i],newroute[j]))
    return newDist-oldDist

def print2OptResult(resultRoute):    
    bestRoute = resultRoute[0]
    bestRoute.extend(resultRoute[1])
    bestRoute.extend(resultRoute[2])
    bestRoute.extend(resultRoute[3])
    print(routecalc(bestRoute))
    print("Time Ended: {}".format(datetime.datetime.now()))

if __name__ == '__main__':
    main()
    with Pool(4) as p:
         results = p.map(argGroup,[(bestRouteQ1,"Task1"),(bestRouteQ2,"Task2"),(bestRouteQ3,"Task3"),(bestRouteQ4,"Task4")])
    print2OptResult(results)
