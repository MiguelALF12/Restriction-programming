from time import time
import itertools


def setConstraint(Const, nomConst, listParameters):
    Const.append([nomConst, [eval('Vars')]+listParameters])


def setVarVals(Vars, Vals):
    Vars['S'] = Vals[0]
    Vars['E'] = Vals[1]
    Vars['N'] = Vals[2]
    Vars['D'] = Vals[3]
    Vars['M'] = Vals[4]
    Vars['O'] = Vals[5]
    Vars['R'] = Vals[6]
    Vars['Y'] = Vals[7]


def evalConst(Const, Vars):
    consist = True
    for i in Const:
        if not(eval(i[0])(*i[1])):
            consist = False
            break
    return consist


def ca1GT(Vars, varName, val):
    if Vars[varName] > val:
        return True
    else:
        return False


def ca1EQ(Vars, varName, val):
    if Vars[varName] == val:
        return True
    else:
        return False


def ca2Sum(Vars, varNames, val, op):
    operands = {'sum': Vars[varNames[0]]+Vars[varNames[1]], 'val': val}
    oper = {'==': 'sum == val', '<=': 'sum <= val',
            '>=': 'sum >= val', '<': 'sum < val', '>': 'sum > val'}
    if eval(oper[op], {"__builtins__": None}, operands):
        return True
    else:
        operands = {'sum': Vars[varNames[0]]+Vars[varNames[1]]+1, 'val': val}
        if eval(oper[op], {"__builtins__": None}, operands):
            return True
        else:
            return False


def ca8Sum(Vars):
    money = 10000*Vars['M']+1000*Vars['O']+100*Vars['N']+10*Vars['E']+Vars['Y']
    send = 1000*Vars['S']+100*Vars['E']+10*Vars['N']+Vars['D']
    more = 1000*Vars['M']+100*Vars['O']+10*Vars['R']+Vars['E']
    if (send+more == money):
        return True
    else:
        return False


fullDom = set(range(10))
Vars = {}
Const = []

# setConstraint(Const,'ca1EQ',['M',1])
setConstraint(Const, 'ca1GT', ['M', 0])
# setConstraint(Const,'ca1EQ',['O',0])
setConstraint(Const, 'ca2Sum', [['N', 'R'], 11, '>'])  # N+R > 11
setConstraint(Const, 'ca8Sum', [])

# fullDom.discard(1)
# fullDom.discard(9)
# fullDom.discard(0)


def prueba():
    for i in itertools.permutations(fullDom, 8):
        # l=tuple([9]+list(i[:3])+[1]+[0]+list(i[3:]))
        setVarVals(Vars, i)
        if evalConst(Const, Vars):
            # print(Vars)
            break
    return Vars


start_time = time()
print(prueba())
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
