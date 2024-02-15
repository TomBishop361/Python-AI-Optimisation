import math
import random
from threading import Thread
import CreateCityArray
import asyncio
import datetime;



currentCities = []
iterations = 5000
startTemperature = 5000
currentTemperature = startTemperature
tasks = []

bestRouteQ1 = []
bestRouteQ2 = []
bestRouteQ3 = []
bestRouteQ4 = []


bestScore = float('inf')
bestRoute = []

async def main():    
    global currentTemperature, currentCities, bestScore , bestRoute,bestRouteQ1,bestRouteQ2 ,bestRouteQ3,bestRouteQ4
    
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

    #asyncio.create_task` are scheduled to run concurrently
    tasks = [ 
        asyncio.create_task(twoOpt1(bestRouteQ1, "Task1")),
        asyncio.create_task(twoOpt1(bestRouteQ2, "Task2")),
        asyncio.create_task(twoOpt1(bestRouteQ3, "Task3")),
        asyncio.create_task(twoOpt1(bestRouteQ4, "Task4")),
    ]
    #When a task i waiting switches to another that is waiting
    await asyncio.gather(*tasks)
    print(tasks)    

    bestRoute =  bestRouteQ1
    bestRoute.extend(bestRouteQ2)
    bestRoute.extend(bestRouteQ3)
    bestRoute.extend(bestRouteQ4)
    #print(bestRoute)
    print(routecalc(bestRoute))
    print("Time Ended: {}".format(datetime.datetime.now()))
    
    

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


async def twoOpt1(route,TaskName):
    best = route
    improved = True
    while improved:
        print(TaskName)
        improved = False
        for i in range(1, len(route) - 2):       
            if i % 100 == 0:
                    print("TwoOpt{} {}".format(TaskName,i))               
            for j in range(i + 1, len(route)):     
                await asyncio.sleep(0)                                       
                if j - i == 1:                    
                    continue
                new_route = route[:]                        
                new_route[i:j] = route[j - 1:i - 1:-1]  # Reverse the segment between i and j
                if objectiveFunction(new_route) < objectiveFunction(best):                    
                    best = new_route
                    improved = True
                    print("Improved {}".format(TaskName))
                    break        
    return best



if __name__ == '__main__':
    #main()
    asyncio.run(main())
    