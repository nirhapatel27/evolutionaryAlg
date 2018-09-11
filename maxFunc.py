import random
from collections import defaultdict


class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

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

    # function is a black box function, we want a function that matches pretty closely to this func
    def max(self, x, y):
        if x > y:
            return x
        else:
            return y

    # gets the function name and the minimum value associated with it from all the cost
    def minVal(self, numDict={}):
        count = 0
        min_value = numDict.get('func0')
        for x, y in numDict.items():
            if min_value > y:
                if y == 0 and count < 5:
                    count = count + 1
                else:
                    min_value = y
                    func = x
        min_value = str(min_value)
        minFunc_dict = {func: min_value}
        return minFunc_dict

    # converts the list to dictionary
    def convert_dict(self, tup, sorted_func):
        for a, b in tup:
            sorted_func.setdefault(a, []).append(b)
        return sorted_func

    # makes a dictionary of first 4 functions with the lowest cost
    def first_population(self, sorted_dict={}):
        first_funcPop = {}
        count = range(0, 4)
        for i in count:
            first_funcPop[list(sorted_dict.keys())[i]] = list(sorted_dict.values())[i]
        print(first_funcPop)
        return first_funcPop

    # sorts the dictionary of the cost in increasing order
    def cost_sort(self, numDict={}):
        sorted_d = sorted(numDict.items(), key=lambda x: x[1])
        return sorted_d

    # finds the cost of each function with respect to the black box function
    def cost(self, func):
        pair_list = range(0, 10)
        cost = 0
        for i in pair_list:
            var1 = random.randint(-100, 100)  # gets random inputs for the two function
            var2 = random.randint(-100, 100)
            cost += (func(var1, var2) - max(var1, var2)) * (func(var1, var2) - max(var1, var2))
        return cost

    # prints the first four functions of the lowest cost and returns the array of thsi function
    def print_firstPop(self, funcList=[], indexArray=[]):
        first_popList = range(0, 4)
        firstPopArr = []
        for i in first_popList:
            firstPopArr.append(funcList[indexArray[i]])
            print(funcList[indexArray[i]])
        return firstPopArr

    # index of the first population functions in the actual dictionary
    def index_firstPop(self, costDict={}, sorted_dict={}):
        indexArr = []
        for i in range(4):
            funcName = list(sorted_dict.keys())[i]
            if funcName in costDict:
                indexArr.append(list(costDict).index(funcName))
        return indexArr

    # finding the nth occurence of a substring
    def findnth(self, string, substring, n):
        parts = string.split(substring, n + 1)
        if len(parts) <= n + 1:
            return -1
        return len(string) - len(parts[-1]) - len(substring)

    # mutates two functions passed in the parameter
    def mutate_population(self, population=[]):
        j = 0
        breedPop = []
        print(len(population))
        while j < len(population):
            strFunc1 = population[j]
            strFunc2 = population[j + 1]
            i = 1
            replaceWord = 'return'
            wordLength = len(replaceWord)
            variableLength = len(' x')
            replaceLen = wordLength + variableLength
            statement1 = self.findnth(strFunc1, replaceWord, 0)
            statement2 = self.findnth(strFunc2, replaceWord, 0)

            while strFunc1[statement1: statement1 + replaceLen] == strFunc2[statement2: statement2 + replaceLen]:
                statement1 = self.findnth(strFunc1, replaceWord, i)
                statement2 = self.findnth(strFunc2, replaceWord, i)
                i += 1
                if i > 3:
                    break

            breedFunc1 = strFunc1.replace(strFunc1[statement1:(statement1 + wordLength + variableLength)],
                                          strFunc2[statement2:(statement2 + wordLength + variableLength)], 1)

            j += 2
            print(breedPop)
            print(j)
            breedPop.append(breedFunc1)
            return breedPop



cfg1 = CFG()
oppr = ['>', '<', '-', '+', '*']
var = ['x', 'y']

# for the number of functions
my_list = range(0, 10)
funcList = []
for i in my_list:
    funcString = """def func{0} ( {1}, {2}):
                strExpr = '{3} {4} {5}'
                expr = eval(strExpr)
                if expr == False:
                    return {6}
                elif expr == True:
                    return {7}
                else:
                    return {8}

            """.format(i, var[0], var[1], var[random.randint(0, 1)],
                       oppr[random.randint(0, 4)], var[random.randint(0, 1)], var[random.randint(0, 1)],
                       var[random.randint(0, 1)], var[random.randint(0, 1)])
    funcList.append(funcString)

# makes new random functions from the oppressions and the variables above
for i in my_list:
    exec(funcList[i])

# gets the cost of each function and adds it to the list
cost_list = []
for i in my_list:
    exec("""cost_list.insert({},cfg1.cost(func{}))""".format(i, i))

cost_dict = {}  # dictionary with the cost and the name of the function
sorted_dict = {}  # sorted dictionary according to their cost in increasing order.

# makes a dictionary and adds the function name and its associated cost
for i in my_list:
    indexStr = str(i)
    funcName = 'func' + indexStr
    cost_dict[funcName] = cost_list[i]

# prints the dictionary with cost and function
print(cost_dict)

# sorts the dictionary and returns a list in ascending order of the cost
sort_list = cfg1.cost_sort(cost_dict)
print(sort_list)

# converts tuple list of func: cost to dictionary
sorted_dict = cfg1.convert_dict(sort_list, sorted_dict)
print(sorted_dict)

# generates the first population (the first 4 members of the sorted function list
cfg1.first_population(sorted_dict)

# gets the index of the first population functions
indexArr = cfg1.index_firstPop(cost_dict, sorted_dict)

# prints all the function in the first population
first_population = cfg1.print_firstPop(funcList, indexArr)

# returns a mutated breed of the first two functions in the first population
breed1 = cfg1.mutate_population(first_population)

