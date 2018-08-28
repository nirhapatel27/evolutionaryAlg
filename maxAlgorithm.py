numList = [2, 3, 10, 12, 17, 123, 34, 200, 134, 28]

import random


# function to find the max in the list
def maxVal():
    max_value = numList[0]
    for x in numList:
        if max_value < x:
            max_value = x
    max_value = str(max_value)
    return max_value


# change the list into string
def stringList():
    geneList = ''.join(map(str, numList))
    geneSet = str(geneList)
    return geneSet


def generate_parent(length):
    genes = []
    geneSet = stringList()
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        # random sample takes sampleSize values from the input without replacement
        genes.extend(random.sample(geneSet, sampleSize))  # appends multiple items to the list
    return ''.join(genes)  # joins genes at the front of ''


# only feedback to guide towards the value, total number of digits in the solution
def get_fitness(target, guess):
    return sum(1 for expected, actual in zip(target, guess)  # zip to iterate over two lists at the same time
               if expected == actual)


# sum returns the total number of digits starting from start and iterating through the number


# function to produce new guess by mutating the current one
def mutate(parent):
    index = random.randrange(0, len(parent))
    childGenes = list(parent)  # converts the parent string to array list
    newGene, alternate = random.sample(stringList(), 2)  # replaces one letter at random from geneSet
    childGenes[index] = alternate \
        if newGene == childGenes[index] \
        else newGene
    # for the alternate replacement if the randomly selected newGene is the same as the one selected earlier
    return ''.join(childGenes)  # recombines the result with a string


def display(guess):
    target = maxVal()
    fitness = get_fitness(target, guess)
    print("{}\t{}".format(guess, fitness))


target = maxVal()
bestParent = generate_parent(len(maxVal()))
bestFitness = get_fitness(target, bestParent)
display(bestParent)

# a loop that generates a guess
while True:  # loops until all the digits in the guess are matched
    child = mutate(bestParent)  # generate a guess
    childFitness = get_fitness(target, child)  # request a fitness for the guess
    if bestFitness >= childFitness:  # compares the fitness of the guess to the best previous guess
        continue
    display(child)  # keeps the guess with better fitness
    if childFitness >= len(bestParent):
        break
    bestFitness = childFitness
    bestParent = child
