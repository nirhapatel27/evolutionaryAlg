import operator
import random
from collections import defaultdict

from pip._vendor.msgpack.fallback import xrange

numList = [2, 3, 10, 12, 17, 123, 34, 200, 134, 28]


# cfg to generate random operations

class CFG(object):
    def __init__(self, val):
        self.prod = defaultdict(list)  # initialises a list
        self.val = val  # constructor initializing the max value

    # finding the difference between the maximum value and number
    def maxDist(self, maxVal):
        dist = abs(self.val - maxVal)
        return dist

    # cleaner way to output the val
    def __repr__(self):
        return "(" + str(self.val) + ")"

    # if the rhs has many numbers separated by |
    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    # generating random numbers for the sentence and operation
    def gen_random(self, symbol):
        sentence = ''

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence


"""
cfg1 = CFG(10)
cfg1.add_prod('Expr', 'Var Oppr Var')  # format of sentence
for j in xrange(10):
    cfg1.add_prod('Var', 'random.randint(1 , 10)')

cfg1.add_prod('Oppr', '+ | - | / | * | <')

for key, value in cfg1.prod.items():
    print(key, value)

for i in xrange(10):
    strExpr = cfg1.gen_random('Expr')
    print(eval(strExpr))
"""


class Number:
    def __init__(self, value):
        self.value = value

    def difference(self, number):
        difference = abs(self.value - number)
        return difference

    def __repr__(self):
        return "(" + str(self.value) + ")"


class Population:

    def initialPopulation(popSize, numList, initialize):
        population = [popSize]

        # looping through the first generation to create create as many difference as possible
        # if population has initialized
        if initialize:
            for i in range(0, popSize):
                population.append(createNum(numList))

        return population


# inverse of route function

class Fitness:

    def __init__(self, absDiff):
        self.absDiff = absDiff
        self.difference = 0
        self.fitness = 0.0

    # getting the difference between each of the numbers in the list
    def numberDifference(self):
        if self.difference == 0:
            numDifference = 0
            for i in range(0, len(self.absDiff)):
                numStart = self.absDiff[i]
                if i + 1 < len(self.absDiff):
                    numFinal = self.absDiff[i + 1]
                else:
                    numFinal = self.absDiff[0]
                numDifference += numStart.difference(numFinal)
            self.difference = numDifference
        return self.difference

    def numberFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.numberDifference())
        return self.fitness

    # creating random numbers, first generation, creating the population


def createNum(numList):
    absDiff = random.sample(numList, len(numList))
    return absDiff


# generating full population


# ranking each fitness to each individual in the population


def rankDiff(population):
    fitnessResults = {}
    for i in range(0, len(population)):
        fitnessResults[i] = Fitness(population[i]).numberFitness()
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)
    # output is the ranked list with id


def geneticAlgorithm(population, popSize):
    pop = initialPopulation(popSize, population)

    print("Final distance: " + str(1 / rankDiff(pop)[0][1]))

    bestRouteIndex = rankDiff(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRoute)
    return bestRoute


cityList = [1, 10, 3, 4, 7, 19]
geneticAlgorithm(population=cityList, popSize=100)
