import operator
import random
from collections import defaultdict

from pip._vendor.msgpack.fallback import xrange


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


# inverse of route function

class Fitness:
    def __init__(self, number):
        self.number = number
        self.difference = 0
        self.fitness = 0.0

    # getting the difference between each of the numbers in the list
    def numberDifference(self):
        if self.difference == 0:
            numDifference = 0
            for i in range(0, len(self.number)):
                numStart = self.number[i]
                if i + 1 < len(self.number):
                    numFinal = self.number[i + 1]
                else:
                    numFinal = self.number[0]
                numDifference += numStart.difference(numFinal)
            self.difference = numDifference
        return self.difference

    def numberFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.numberDifference())
        return self.fitness

    # creating random numbers, first generation, creating the population

    def createNum(self, numList):
        number = random.sample(numList, len(numList))
        return number

    # generating full population

    def initialPopulation(self, listSize, numList):
        population = []

        # looping through the first generation to create create as many difference as possible
        for i in range(0, listSize):
            population.append(self.createNum(numList))
        return population

    # ranking each fitness to each individual in the population

    def rankDiff(self, population):
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).numberFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)
        # output is the ranked list with id

    def geneticAlgorithm(self, population, popSize):
        pop = self.initialPopulation(popSize, population)

        print("Final distance: " + str(1 / self.rankDiff(pop)[0][1]))
        bestRouteIndex = self.rankDiff(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        print(bestRoute)
        return bestRoute


fitness = Fitness(10)
cityList = [1, 10, 3, 4, 7, 19]
fitness.geneticAlgorithm(population=cityList, popSize=100)
