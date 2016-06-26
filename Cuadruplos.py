

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
 
cuadruplo = []
Temporales = []
pilaO = [] 		# Pila de operandos
pOper = [] 		# Pila de operadores
PTipos = []		# Pila de tipos
PSaltos = []	# Pila de saltos
cont = 1
HERE = 0
PC = []
pOper.append('[')

PC.append(cont)

cuadruplo = []
listaQuad = []
SumaResta = []
CondSumaResta = []
Condicional = []
Temporales = []
pilaO = [] 		# Pila de operandos
pOper = [] 		# Pila de operadores
PTipos = []		# Pila de tipos
PSaltos = []	# Pila de saltos
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
	global listaQuad

	# print ('A is: ', tipo)
	# print ('ARGS: ', args)
	notPopedYet=True
	# print(*args)
	
	if tipo == 'metodo_principal':	
		pass
	elif tipo == 'asignacion':
		if not isinstance(args[1], (list, tuple)):
			cuadruplo.append("=")
			cuadruplo.append(args[0])
			cuadruplo.append(args[1])
			PC += 1
			listaQuad = listaQuad, cuadruplo
			
		elif isinstance(args[1], str):
			cuadruplo.append("=")
			cuadruplo.append(args[0])
			cuadruplo.append(args[1])
			PC += 1
			listaQuad = listaQuad, cuadruplo
			

	elif tipo == 'END':
		pass
	cuadruplo = []
	print(listaQuad)