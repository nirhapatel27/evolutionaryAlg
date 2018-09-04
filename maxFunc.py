import operator
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

    def max(self, x, y):
        if x > y:
            return x
        else:
            return y

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

    def convert_dict(self, tup, sorted_func):
        for a, b in tup:
            sorted_func.setdefault(a, []).append(b)
        return sorted_func

    def first_population(self, sorted_dict={}):
        first_funcPop = {}
        count = range(0, 4)
        for i in count:
            first_funcPop[list(sorted_dict.keys())[i]] = list(sorted_dict.values())[i]
        print(first_funcPop)


    def cost_sort(self, numDict={}):
        sorted_d = sorted(numDict.items(), key=lambda x: x[1])
        return sorted_d

    def cost_max(self, func):
        pair_list = range(0, 10)
        cost = 0
        for i in pair_list:
            var1 = random.randint(-100, 100)
            var2 = random.randint(-100, 100)
            cost += (func(var1, var2) - max(var1, var2)) * (func(var1, var2) - max(var1, var2))
        return cost

    def mutate_max(self, func1, func2):
        return


cfg1 = CFG()
cfg1.add_prod('S', '''\n\tif VAR OPPR VAR :\n\t\tprint( VAR ); else: \n\t\tprint( VAR )\n''')
cfg1.add_prod('VAR', '1 | 2')
cfg1.add_prod('OPPR', '> | < | + | - | *')

str1 = cfg1.gen_random('S')
oppr = ['>', '<', '-', '+', '*']
var = ['x', 'y']
# print(str1)
# compiledCodeBlock = compile(str1, '<string>', 'single')
# exec(compiledCodeBlock)
# eval(str1)

my_list = range(0, 100)
for i in my_list:
    exec("""def func{} ( {}, {}):
               strExpr = '{} {} {}'
               #print(strExpr)
               expr = eval(strExpr)
               if expr == False:
                   return {}
               elif expr == True:
                   return {}
               else:
                   return {}

           """.format(i, var[0], var[1], var[random.randint(0, 1)],
                      oppr[random.randint(0, 4)], var[random.randint(0, 1)], var[random.randint(0, 1)],
                      var[random.randint(0, 1)], var[random.randint(0, 1)]))

for i in my_list:
    exec("""func{}(random.randint(0, 10), random.randint(0, 10))""".format(i))

cost_list = []
for i in my_list:
    exec("""cost_list.insert({},cfg1.cost_max(func{}))""".format(i, i))

cost_dict = {}
sorted_dict = {}

for i in my_list:
    indexStr = str(i)
    funcName = 'func' + indexStr
    cost_dict[funcName] = cost_list[i]

print(cost_dict)
sort_list = cfg1.cost_sort(cost_dict)
print(sort_list)
sorted_dict = cfg1.convert_dict(sort_list, sorted_dict)
print(sorted_dict)
print(cfg1.minVal(cost_dict))
cfg1.first_population(sorted_dict)
