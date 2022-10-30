import numpy as np
from time import time


Casillas = {}
Restric = {'Filas': [],
           'Columnas': [],
           'Regiones': []
           }
fullDom = {1, 2, 3, 4, 5, 6, 7, 8, 9}
NonDefinedBoxes = []


def loadNewVals():
    global Casillas, NonDefinedBoxes
    archivo = open('./boards/tableroImposible.txt', 'r')
    for pos in range(81):
        linea = archivo.readline()
        Casillas[pos] = {'dom': {int(linea[0])}, 'values': None, 'restric':
                         {
            'Fila': None,
            'Columna': None,
            'Region': None,
        }}
        if Casillas[pos]['dom'] == {0}:
            NonDefinedBoxes.append(pos)
            Casillas[pos]['values'] = fullDom.copy()


def setConstraints():
    global Casillas, Restric
    for i in range(0, 9):
        ind = i*9
        lcasillas = [ind+0, ind+1, ind+2, ind +
                     3, ind+4, ind+5, ind+6, ind+7, ind+8]
        Restric['Filas'].append(lcasillas)
        for j in lcasillas:
            Casillas[j]['restric']['Fila'] = lcasillas
        lcasillas = []

    for i in range(0, 9):
        lcasillas = [i+0, i+9, i+18, i+27, i+36, i+45, i+54, i+63, i+72]
        Restric['Columnas'].append(lcasillas)
        for j in lcasillas:
            Casillas[j]['restric']['Columna'] = lcasillas
        lcasillas = []

    for i in range(0, 3):
        posi = i * 27
        for j in range(0, 3):
            posj = posi + (j*3)
            lcasillas = [posj+0, posj+9, posj+18, posj+1, posj+10, posj+19,
                         posj+2, posj+11, posj+20]
            Restric['Regiones'].append(lcasillas)
            for z in lcasillas:
                Casillas[z]['restric']['Region'] = lcasillas
            lcasillas = []


def pruebaInit(Casillas, Restric):
    lista = Casillas.items()

    for i in lista:
        print(i, "\n")

    print("\n")

    restric = Restric.items()

    for i in restric:
        print(i, "\n")


def showSudoku(Casillas):

    for i in range(9):
        ind = i * 9
        l = [Casillas[ind+0]['dom'], Casillas[ind+1]['dom'], Casillas[ind+2]['dom'],
             Casillas[ind+3]['dom'], Casillas[ind +
                                              4]['dom'], Casillas[ind+5]['dom'],
             Casillas[ind+6]['dom'], Casillas[ind+7]['dom'], Casillas[ind+8]['dom']]
        print(np.array(l))
    print("\n")


def posibleValues():
    global Casillas, NonDefinedBoxes

    for i in NonDefinedBoxes:
        L = Casillas[i]['values'].copy()
        if Casillas[i]['dom'] == {0}:
            for j in L:
                #k = L[j]
                posibleValueForGeneral(i, j)


def posibleValueForGeneral(casilla, valor):
    global Casillas
    for i in Casillas[casilla]['restric']['Fila']:  # recorre las restricciones de filas
        if Casillas[i]['dom'] == {valor} and valor in Casillas[casilla]['values']:
            Casillas[casilla]['values'].remove(valor)
            return
    # recorre las restricciones de columnas
    for i in Casillas[casilla]['restric']['Columna']:
        if Casillas[i]['dom'] == {valor} and valor in Casillas[casilla]['values']:
            Casillas[casilla]['values'].remove(valor)
            return
    # recorre las restricciones de Areas
    for i in Casillas[casilla]['restric']['Region']:
        if Casillas[i]['dom'] == {valor} and valor in Casillas[casilla]['values']:
            Casillas[casilla]['values'].remove(valor)
            return


def OnePossibleValueCond():
    global Casillas, NonDefinedBoxes

    if len(NonDefinedBoxes) == 0:
        return
    else:
        L = NonDefinedBoxes.copy()
        tam = len(L)
        for i in L:
            if len(Casillas[i]['values']) == 1:
                Casillas[i]['dom'].clear()
                Casillas[i]['dom'] = Casillas[i]['dom'] | Casillas[i]['values']
                Casillas[i]['values'] = None
                NonDefinedBoxes.remove(i)
                posibleValues()
        if tam != len(NonDefinedBoxes):
            OnePossibleValueCond()
        else:
            return


def TwoSamePossibleValuesCond(area):
    global Casillas, NonDefinedBoxes, Restric
    copiaCasillas = {}
    val = False
    for parametro in Restric[area]:
        for i in parametro:
            for j in parametro:
                if i != j and (Casillas[i]['dom'] == {0} and Casillas[j]['dom'] == {0}):
                    if (Casillas[i]['values'] == Casillas[j]['values']) and (len(Casillas[i]['values']) == 2):
                        for z in parametro:
                            if Casillas[z]['dom'] == {0}:
                                if z != i and z != j:
                                    l = list(Casillas[i]['values'])[0]
                                    k = list(Casillas[i]['values'])[1]
                                    if l in Casillas[z]['values']:
                                        if len(Casillas[z]['values']) == 1:
                                            Casillas = copiaCasillas
                                            val = False
                                            return val
                                        else:
                                            copiaCasillas = Casillas.copy()
                                            val = True
                                            Casillas[z]['values'].remove(l)
                                    if k in Casillas[z]['values']:
                                        if len(Casillas[z]['values']) == 1:
                                            Casillas = copiaCasillas
                                            val = False
                                            return val
                                        else:
                                            copiaCasillas = Casillas.copy()
                                            val = True
                                            Casillas[z]['values'].remove(k)
    return val


def graciasCamilo():
    global Casillas, Restric, NonDefinedBoxes
    val = True
    while val:
        posibleValues()  # Cargamos cada casilla con sus posibles valores
        # hacemos cada casilla cn un solo valor posible, como su nuevo dominio
        OnePossibleValueCond()
        for i in list(Restric.keys()):
            val = TwoSamePossibleValuesCond(i)
        if val:
            continue
        else:
            solve()


def solve():
    global Casillas, NonDefinedBoxes
    for i in NonDefinedBoxes:
        if Casillas[i]['dom'] == {0}:
            for j in Casillas[i]['values']:
                if posibleValue(Casillas, i, j):
                    Casillas[i]['dom'] = {j}
                    solve()
                    Casillas[i]['dom'] = {0}
            return
    print("Sudoku resuelto: \n")
    showSudoku(Casillas)


def posibleValue(Casillas, casilla, valor):

    if Casillas[casilla]['dom'] == {0}:
        # recorre las restricciones de filas
        for i in Casillas[casilla]['restric']['Fila']:
            if Casillas[i]['dom'] == {valor}:
                return False
        # recorre las restricciones de columnas
        for i in Casillas[casilla]['restric']['Columna']:
            if Casillas[i]['dom'] == {valor}:
                return False
        # recorre las restricciones de Areas
        for i in Casillas[casilla]['restric']['Region']:
            if Casillas[i]['dom'] == {valor}:
                return False
        return True
    else:
        print("Error, casilla invalida")
        return False


# inicialización de casillas y nuevos valores
loadNewVals()

# inicialización de restricciones
setConstraints()

# verificar la inicialización de casillas es correcta
pruebaInit(Casillas, Restric)

# Mostrar el sudoku
showSudoku(Casillas)


# probar si un valor es posible
# print(posibleValue(Casillas,Restric,1,2))

# solución
start_time = time()
graciasCamilo()
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)


#
