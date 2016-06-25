

from Var_Table import *
from cubo import *
import sys
Matricial = []
Temporal = 0
 
Avail = []      # Pila de temporales
globaltable = tablaVars() # (entero -> 0), (real -> 5001), (char -> 10000),
 
#                       entero  real  char  
localtable = tablaVars(25001, 30001, 45001)
 
#                            entero   real  char
tablaTemporales = tablaVars(70001, 85000, 90000)
file = open("CodigoFinal.txt", "w")
 
file.write("\n")
file.write("\n")
 
cuadruplo = []
Temporales = []
pilaO = []      # Pila de operandos
pOper = []      # Pila de operadores
PTipos = []     # Pila de tipos
PSaltos = []    # Pila de saltos
cont = 1
HERE = 0
PC = []
pOper.append('[')
 
PC.append(cont)
 
def quad(tipo, *args):
	operador = []
cuadruplo = []
SumaResta = []
CondSumaResta = []
Condicional = []
Temporales = []
pilaO = []      # Pila de operandos
pOper = []      # Pila de operadores
PTipos = []     # Pila de tipos
PSaltos = []    # Pila de saltos
cont = 0
HERE = 0
PC = 0
pOper.append('[')
 
 
def quad(tipo, *args):
	global cont
	global PC
	global notPopedYet
	global HERE
	global cuadruplo
#   print ('A is: ', tipo)
#   print ('ARGS: ', args)
	notPopedYet=True
	print(tipo)
	# if tipo == 'asignacion':
	# 	Operador = args[0]
	# 	if args[2] == None:
	# 		Operando2 = args[1]
	# 		Operando1 = pilaO.pop()
	# 		cuadruplo.append(Operador)
	# 		cuadruplo.append(Operando1)
	# 		cuadruplo.append(Operando2)

	# 	else:
	# 		Operador = args[0]
	# 		Operando2 = args[1]
	# 		Operando1 = args[2]
	# 		cuadruplo.append(Operador)
	# 		cuadruplo.append(Operando1)
	# 		cuadruplo.append(Operando2)
 
#       print(cuadruplo)
#       PC.append(cont)
#       num = 0
#       file = open("TextSalida.txt", "w")
#       file = open("Ensamblador.txt", "w")
       
#       file.write(str(cuadruplo))
 
       
        
		# print(cuadruplo)