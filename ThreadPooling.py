import math
import random
import tracemalloc
from threading import Thread
import asyncio
import CreateCityArray
import datetime;
import concurrent.futures

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

def main():    
    global currentTemperature, currentCities, bestScore , bestRoute, bestRouteQ1,bestRouteQ2 ,bestRouteQ3,bestRouteQ4
    
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

    #creates a a pool for 4 cores and assigns a task to each one
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #Submit tasks for each quater
        task1 = executor.submit(twoOpt1, bestRouteQ1, "Task1")
        task2 = executor.submit(twoOpt1, bestRouteQ2, "Task2")
        task3 = executor.submit(twoOpt1, bestRouteQ3, "Task3")
        task4 = executor.submit(twoOpt1, bestRouteQ4, "Task4")

    #gathers the results from all tasks
    results = [task1.result(), task2.result(), task3.result(), task4.result()]
    
    #res1,res2,res3,res4 = await asyncio.gather(twoOpt1(bestRouteQ1,"Task1"),twoOpt1(bestRouteQ2,"Task2"),twoOpt1(bestRouteQ3,"Task3"),twoOpt1(bestRouteQ4,"Task4"))
    bestRoute =  results[0]
    bestRoute.extend(results[1])
    bestRoute.extend(results[2])
    bestRoute.extend(results[3])
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

#https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python
def twoOpt1(route,TaskName):
    best = route
    improved = True
    while improved:
        print(TaskName)
        improved = False
        for i in range(1, len(route) - 2):      
            #every 100 print
            if i % 100 == 0:
                    print("TwoOpt{} {}".format(TaskName,i))                 
            for j in range(i + 1, len(route)):  
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
    main()
   # asyncio.run(main())
    
