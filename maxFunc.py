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

    def minVal(self, numList=[]):
        count = 0
        min_value = numList[0]
        for x in numList:
            if min_value > x:
                if x == 0 and count < 5:
                    count = count + 1
                else:
                    min_value = x
        min_value = str(min_value)
        return min_value

    def cost_max(self, func):
        pair_list = range(0, 10)
        cost = 0
        for i in pair_list:
            var1 = random.randint(-100, 100)
            var2 = random.randint(-100, 100)
            cost += (func(var1, var2) - max(var1, var2)) * (func(var1, var2) - max(var1, var2))
        return cost


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
                   return expr

           """.format(i, var[0], var[1], var[random.randint(0, 1)],
                      oppr[random.randint(0, 4)], var[random.randint(0, 1)], var[random.randint(0, 1)],
                      var[random.randint(0, 1)]))

for i in my_list:
    exec("""func{}(random.randint(0, 10), random.randint(0, 10))""".format(i))

cost_list = []
for i in my_list:
    exec("""cost_list.insert({},cfg1.cost_max(func{}))""".format(i, i))
print(cost_list)
print(cfg1.minVal(cost_list))
