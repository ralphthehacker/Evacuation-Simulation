from random import randint
import numpy as np

#place holder constants
from scipy.stats import chisquare

numbersList = []
possibleNumbers = 100
numOfIterIncrease = 10
numOfIter = 10
totalRange = 5

for i in range(0, 5):
    tempList = []
    for i in range(0, numOfIter):
        tempList.append(randint(0, possibleNumbers))
    numbersList.append(tempList)
    numOfIter *= numOfIterIncrease

numOfIter = 10
for observed in numbersList:
    data = np.array(observed)
    print "(chi squared statistic, p-value) with", numOfIter, "samples generated: ", chisquare(data)
    numOfIter *= numOfIterIncrease