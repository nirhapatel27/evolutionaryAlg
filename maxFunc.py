import random
from collections import defaultdict

from pip._vendor.msgpack.fallback import xrange

numList = [2, 3, 10, 12, 17, 123, 34, 200, 134, 28]


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

    def maxVal(self):
        max_value = numList[0]
        for x in numList:
            if max_value < x:
                max_value = x
        max_value = str(max_value)
        return max_value


cfg1 = CFG()
cfg1.add_prod('S', '''\n\tif VAR OPPR VAR :\n\t\tprint( VAR )\n\telse: \n\t\tprint( VAR )\n''')
cfg1.add_prod('VAR', '1 | 2')
cfg1.add_prod('OPPR', '> | <')

str1 = cfg1.gen_random('S')
oppr = ['>', '<', '+', '-', '*', '/']
var = ['x', 'y']
# print(str1)
# compiledCodeBlock = compile(str1, '<string>', 'single')
# exec(compiledCodeBlock)
# eval(str1)

my_list = range(0, 100)
for i in my_list:
    exec("""
def func{} ( {}, {}, my_List = {}):
        strExpr = '{} {} {}'
        #print(strExpr)
        expr = eval(strExpr)
        if expr == False or expr == True:
            print(expr)
        else:
            return
            #print("regular")

    """.format(i, var[0], var[1], numList, var[random.randint(0, 1)],
               oppr[random.randint(0, 5)], var[random.randint(0, 1)]))

for i in my_list:
    exec("""func{}(random.randint(0, 10), random.randint(0, 10))""".format(i))

"""func1(random.randint(0, 10), random.randint(0, 10))
func2(random.randint(0, 10), random.randint(0, 10))
func3(random.randint(0, 10), random.randint(0, 10))
func4(random.randint(0, 10), random.randint(0, 10))
func5(random.randint(0, 10), random.randint(0, 10))
func6(random.randint(0, 10), random.randint(0, 10))"""

"""var[random.randint(0, 1)],
               var[random.randint(0, 1)]"""

# if {} {} {}:
# print({})
# else:
# print({})
