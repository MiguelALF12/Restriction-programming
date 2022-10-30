import time

import os

"""inicializa todas las variables que se usaran"""
fullDom = {1, 2, 3, 4, 5, 6, 7, 8, 9}
Casillas = {}
copiaCasillas = []
Restric = {}
newVals = []
ceroVals = []
Copia = {}

"""inicializa el diccionario  casillas"""
for i in range(81):
    Casillas[i] = {'dom': fullDom.copy(), 'rest': {'row': None,
                                                   'col': None, 'reg': None, 'other': {}}}


"""carga los valores del sudoku """


def loadBoard(Casi):
    archivo = open('tableroDificil.txt', 'r')
    curNewVals = []
    for pos in range(81):
        linea = archivo.readline()
        if(linea[0] != '0'):
            Casi[pos]['dom'] = {int(linea[0])}
            curNewVals.append(pos)
        else:
            ceroVals.append(pos)

    return curNewVals


"""construccion de las restricciones con aridad 9"""


def ConstrainBuilder(Casi, rest):
    if not(9 in rest):
        rest[9] = {'rows': [], 'cols': [], 'regs': []}
    for i in range(0, 9):
        ind = i*9
        lcasillas = [ind+0, ind+1, ind+2, ind +
                     3, ind+4, ind+5, ind+6, ind+7, ind+8]
        rest[9]['rows'].append(['<>', lcasillas])
        for pos in lcasillas:
            Casi[pos]['rest']['row'] = i

        lcasillas = [i+0, i+9, i+18, i+27, i+36, i+45, i+54, i+63, i+72]
        rest[9]['cols'].append(['<>', lcasillas])
        for pos in lcasillas:
            Casi[pos]['rest']['col'] = i
    r = 0
    for i in range(0, 3):
        posi = i*27
        for j in range(0, 3):
            posj = posi+(j*3)
            lcasillas = [posj+0, posj+1, posj+2, posj+9,
                         posj+10, posj+11, posj+18, posj+19, posj+20]
            rest[9]['regs'].append(['<>', lcasillas])
            for pos in lcasillas:
                Casi[pos]['rest']['reg'] = r
            r = r+1


"""Evalua si  se puedo encontrar dominios de 1 """


def delValRest(Casi, CasiRestList, Val, curCasi, CasiVals):
    curNewVals = []

    for i in CasiRestList[1]:
        if i != curCasi:
            if not(i in CasiVals):
                if(len(Casi[i]['dom']) == 1):
                    curNewVals.append(i)
            if(Val in Casi[i]['dom']):
                Casi[i]['dom'].discard(Val)
                if(len(Casi[i]['dom']) == 1):
                    curNewVals.append(i)
    return curNewVals


""" encunetra dominios doble y descarta a otros dominios"""


def NewdelValRest(Casi, Rest):
    curNewVals = []

    for res in Rest:
        RestEval = res[1]
        for i in RestEval:
            for j in RestEval:
                if(i != j):
                    if(Casi[i]['dom'] == Casi[j]['dom']):
                        if(len(Casi[j]['dom']) == 2):
                            for p in RestEval:
                                if(len(Casi[p]['dom']) != 1):
                                    if((p != i) and (p != j)):
                                        l = list(Casi[j]['dom'])[0]
                                        k = list(Casi[j]['dom'])[1]
                                        if(l in Casi[p]['dom']):
                                            Casi[p]['dom'].discard(l)
                                        if(k in Casi[p]['dom']):
                                            Casi[p]['dom'].discard(k)
                                        if(len(Casi[p]['dom']) == 1):
                                            curNewVals.append(p)

    curNewVals = list(set(curNewVals))
    return curNewVals


"""evalue las restricciones y cosistencias por fila,columna y region """


def Consist4newVals(Casi, Rest, nVals, CasiVals):
    curNewVals = []
    for curCasi in nVals:
        curVal = list(Casi[curCasi]['dom'])[0]
        curNewVals = curNewVals + \
            delValRest(Casi, Rest[9]['rows'][Casi[curCasi]
                       ['rest']['row']], curVal, curCasi, CasiVals)
        curNewVals = curNewVals + \
            delValRest(Casi, Rest[9]['cols'][Casi[curCasi]
                       ['rest']['col']], curVal, curCasi, CasiVals)
        curNewVals = curNewVals + \
            delValRest(Casi, Rest[9]['regs'][Casi[curCasi]
                       ['rest']['reg']], curVal, curCasi, CasiVals)

    if(len(curNewVals) == 0):
        curNewVals = curNewVals+NewdelValRest(Casi, Rest[9]['rows'])
        curNewVals = curNewVals+NewdelValRest(Casi, Rest[9]['cols'])
        curNewVals = curNewVals+NewdelValRest(Casi, Rest[9]['regs'])

    return curNewVals


def possibleValue(Casillas, casilla, valor, Restric):
    for i in (list(Restric[9]['rows'][Casillas[casilla]['rest']['row']])[1]):
        if len(Casillas[i]['dom']) == 1:
            if valor == list(Casillas[i]['dom'])[0]:
                return False
    for i in (list(Restric[9]['cols'][Casillas[casilla]['rest']['col']])[1]):
        if len(Casillas[i]['dom']) == 1:
            if valor == list(Casillas[i]['dom'])[0]:
                return False
    for i in (list(Restric[9]['regs'][Casillas[casilla]['rest']['reg']])[1]):
        if len(Casillas[i]['dom']) == 1:
            if valor == list(Casillas[i]['dom'])[0]:
                return False
    return True


def solucion():
    global Casillas, copiaCasillas
    global Restric
    global ceroVals
    for i in ceroVals:
        if len(Casillas[i]['dom']) > 1:
            copiaCasillas = list(Casillas[i]['dom'])
            for j in Casillas[i]['dom']:
                if possibleValue(Casillas, i, j, Restric):
                    Casillas[i]['dom'] = {j}
                    solucion()
                    Casillas[i]['dom'].clear()
                    Casillas[i]['dom'] = copiaCasillas
            return


newVals = loadBoard(Casillas)
ConstrainBuilder(Casillas, Restric)
CasiVals = newVals.copy()


"""resuelve el sudoku"""
while True:
    newVals = Consist4newVals(Casillas, Restric, newVals, CasiVals)
    if(len(newVals) == 0):
        ceroVals.sort()
        solucion()
        break
    else:
        CasiVals = CasiVals+newVals
        CasiVals = list(set(CasiVals))
        ceroVals = set(ceroVals)
        CasiVals = set(CasiVals)
        NewValors = ceroVals.difference(CasiVals)
        NewValors = list(NewValors)
        CasiVals = list(CasiVals)
        ceroVals = list(ceroVals)
        ceroVals = NewValors.copy()
        NewValors = list(NewValors)

# print(Restric)

"""imprime el sudoku solucionado"""
y = 0

for i in range(0, 9):
    print('\n-------------------------------------')
    print("| ", end="")
    for j in range(0, 9):
        p = list(Casillas[y]['dom'])
        y = y+1
        print(p[0], end=" | ")
print('\n-------------------------------------')
