"""CSP 

Conjunto de Variables
Conjunto de dominios
Conjunto de Restricciones

De forma algoritmica se construye el resolutor:
Aplicar Consistencia
Aplpicar algoritmos de búsqueda

Matrices Hash 

"""
FullDom={1,2,3,4,5,6,7,8,9}
Casillas={}

for i in range(81):
  Casillas[i]=FullDom.copy()

#print(Casillas)


import os
archivo = open('tablero.txt', 'r')
kv=""
for linea in archivo:
  kv=linea
  kv=kv.split(":")
  #print(kv)
  Casillas[int(kv[0])]={int(kv[1][0])}
  """print("La llave" es "+str(int(kv[0]))+" y el valor es "+str(int(kv[1][0])))"""

#Construye las restricciones de fila
Restric=[]
for i in range(0,9):
  ind=i*9
  lcasillas=[ind+0,ind+1,ind+2,ind+3,ind+4,ind+5,ind+6,ind+7,ind+8];
  Restric.append(['<>',lcasillas])
  lcasillas=[]

#Restric => ["<>",[0,9,18,27,36,45,54,63,72]]
for i in range(0,9):
  lcasillas=[i+0,i+9,i+18,i+27,i+36,i+45,i+54,i+63,i+72];
  Restric.append(['<>',lcasillas])

# print(len(Casillas))

# print(Casillas.keys())

Lista1 = []			# se crean listas inciiales para almacenar
Lista2 = []			#valores de cada columna para area 3x3
Lista3 = []

for i in range(0,9): #se escoge cada columna y se agrega a una lista
	ind = i 
	Lista1.append([ind+0,ind+9,ind+18])
	Lista2.append([ind+27,ind+36,ind+45])
	Lista3.append([ind+54,ind+63,ind+72])

Lista1F = []		#Listas finales que separaran todas las tripletas
Lista2F = []		#de areas
Lista3F = []
Lista1aux = []
Lista2aux =[]
Lista3aux = []
# Lista1aux.extend(Lista1[0:3])
# print(Lista3aux)
for i in range(0, 9, 3): #separación en tripletas
    Lista1F.append(Lista1[i:i+3])
    Lista2F.append(Lista2[i:i+3])
    Lista3F.append(Lista3[i:i+3])
Listanueva = []
Listanueva.append(Lista1F[0][0]+Lista1F[0][1]+Lista1F[0][2])
print(Listanueva)

