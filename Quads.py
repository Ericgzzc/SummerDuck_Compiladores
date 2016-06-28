from Symboltable import *
from cubo import *
import numbers
import json 
import sys
from copy import deepcopy

class Quads(object):
	global file 	
	file = open("CodigoIntermedio.txt", "w")

	def __init__(self,tree):
		self.symbolTable = SymbolTable(None, 'global')
		self.arbol = tree
		programa, nombre, *args, principal = self.arbol;
		self.programa = programa
		self.nombre = nombre
		self.principal = principal
		if len(args) == 2:
			self.dec_val = args[0]
			self.dec_fun = args[1]
		elif len(args) == 1:
			if args[0][0] == 'declara_funciones':
				self.dec_fun = args[0]
				self.dec_val = []
			else:
				self.dec_val = args[0]
				self.dec_fun = []
		else:
			self.dec_fun = []
			self.dec_val = []
		self.quad(programa, nombre)
		self.declaraVariables(self.dec_val, "global", self.symbolTable)
		self.declaraFunciones(self.symbolTable)
		
		self.metodo_principal(principal,self.symbolTable)

	def metodo_principal(self,principal, table):
		principal_nomb, *args = principal
		
		self.quad(principal_nomb)
		if len(args) == 2:
			self.declaraVariables(args[0], principal_nomb, table)
			self.estatutos(args[1], table)
		else:
			if args[0][0] == 'declaracion_variables':
				self.declaraVariables(args[0], principal_nomb,table)
			else:
				self.estatutos(args[0], table)
		
	def declaraVariables(self,dec_val,var_tipo, table):
	
		if dec_val:
			while dec_val[1]:
				tipo = dec_val[1].pop(0)
				variables = dec_val[1].pop(0)
				for x in variables:
					if (not table.put(VariableSymbol(x, tipo))):
						print (var_tipo + '    '+ x+' alreday declared')
					self.quad("declaracion_variables", tipo,var_tipo, x)
		

	def getParametros(self,dec_val):
		param = []
		parame = dec_val
		if parame:
			while parame[1]:
				tipo = parame[1].pop(0)
				variables = parame[1].pop(0)
				for x in variables:
						param = param + [x,]
		return param

	def modulos(self,dec_fun):
		modulos = []
		temp = []
		if dec_fun:
			while dec_fun:
				b = dec_fun.pop(0)
				if b != "END":
					temp = temp + [b]
				else:
					modulos= modulos + [temp,]
					temp = []
		return modulos
	def estatutos(self, estatutos, table):
		estatutos.pop(0)
		while estatutos[0]:
			x = estatutos[0].pop(0)
			if x[0] == 'asignacion':
				self.asignacion(x, table)
			if x[0] == 'decision':
				self.decision(x, table)
			if x[0] == 'repeticion':
				y = x.pop(1)
				if y[0]=='mientras':
					self.mientras(y, table)
				if y[0]=='repite':
					self.repite(y, table)
			if x[0] == 'llamada':
				self.llamada(x,table)
			if x[0] == 'lectura':
				self.lectura(x,table)
			if x[0] == 'escritura':
				self.escritura(x, table)

	def escritura(self, llam,table):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def lectura(self, llam,table):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def existenVariables(self, param, table):
		print("here1")

	def llamada(self, llam, table):
		symbol = table.get(llam[1])
		functable =  SymbolTable(table, symbol)
		
		if isinstance(symbol, FunctionSymbol):
			if len(symbol.arguments) != len(llam[2]):
				print('Llamada  ' + llam[1] + '  expected '+ str(len(symbol.arguments)) + ' arguments')
			else:	
				pass
				exptectedTypes = [table.get(arg).type for arg in symbol.arguments]
				types = []
				for arg in llam[2]:
					if table.get(arg):
						types = types + [table.get(arg).type,]
					else:
						print('Variable  ' + arg + '  No declaraded')
				
				if len(exptectedTypes) == len(types):
					for exprType, expectedType, i in zip(types, exptectedTypes,range(1, len(types) + 1)):
						if exprType != expectedType and not (exprType == 'int' and expectedType == 'float'):
							print ('Incorrect type of parameter, expected '+expectedType+", found "+exprType)
				


		if symbol == None:
			print('modulo  ' + llam[1] + '  No declared' )

		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def repite(self,rep, table):		
		repite, hacer, exp = rep
		hacer = hacer.pop()
		self.quad(repite)
		self.estatutos(hacer, table)
		self.quad("hasta", exp)
	
	def mientras(self,whil, table):
		mientras, exp, hacer = whil
		self.quad(mientras, exp)
		hacer = hacer.pop()
		self.estatutos(hacer, table)
		self.quad("end_control", "end_mientras")

	def decision(self, dec, table):
		dec.pop(0)
		if len(dec) == 3:
			si, exp, hacer = dec
			self.quad(si, exp)
			hacer = hacer.pop()
			self.estatutos(hacer, table)
			self.quad("end_control", "end_si")
		else:
			si, exp, hacer, sino, hacer2 = dec
			self.quad(si, exp)
			hacer = hacer.pop()
			self.estatutos(hacer, table)
			self.quad(sino,)
			hacer2 = hacer2.pop()
			self.estatutos(hacer2, table)
			self.quad("end_control", "end_sino")
			self.quad("end_control", "end_si")
		
	def checarOperacion(self,a,b,op, table):
		operando1 = table.get(a)
		operando2 = table.get(b)
		
		if operando1 != None and operando2 != None:
			result = cubo[operando1.type][operando2.type][op]
			if result != 'Error':
				return(result)
			else:
				print("Cant do operation  " + str(a) + " " + str(op) + " " + str(b)+ "incompatyble types")
				return("error")
		
		elif operando1 == None and operando2 == None:

				if isinstance(b, int) and isinstance(a, int):
					result = cubo["entero"]["entero"][op]
					return(result)
				elif isinstance(b, float) and isinstance(a, float):
					result = cubo["real"]["float"][op]
					return(result)
				elif isinstance(b, int) and isinstance(a, float):
					result = cubo["real"]["entero"][op]
					return(result)
				elif isinstance(b, float) and isinstance(a, int):
					result = cubo["entero"]["real"][op]
					return(result)
				else:
					print("Variable  " + str(b)  + "  No declared")
					return("error")
		elif operando1 == None:
				print(isinstance(a, numbers.Real))
				print("Variable  " + str(a) + "  No declared")
				return("error")



	def asignacion(self, asig, table):
		resultado = ""
		a = table.get(asig[1]);
		if a == None:
			print('Variable  ' + asig[1] + '  No declared')
		else:
			if isinstance(asig[2], list):
				operacion = deepcopy(asig[2])
				if isinstance(operacion[3], list):
					while isinstance(operacion[3], list):
						operacion = operacion.pop()
						resultado = self.checarOperacion(operacion[2],operacion[3], operacion[1],table)
						if resultado != "error":
							if cubo[resultado][a.type]["="] != a.type:
								print("Cant assign incomptyble types  " + str(a.name) + " exptected " + str(a.type) + " given " + str(resultado))
						
				else:
					resultado = self.checarOperacion(operacion[2],operacion[3], operacion[1],table)
					if resultado != "error":
						if cubo[resultado][a.type]["="] != a.type:
							print("Cant assign incomptyble types  " + str(a.name) + " exptected " + str(a.type) + " given " + str(resultado))
			else:
				if isinstance(asig[2], int):
					resultado = cubo["entero"][a.type]["="]
				elif isinstance(asig[2], float):
					resultado = cubo["real"][a.type]["="]
				else:
					resultado = cubo["char"][a.type]["="]
				if resultado != a.type:
					print("Cant assign incomptyble types  " + str(a.name) + " exptected " + str(a.type) + " given " + str(resultado))

		self.quad(asig[0], asig[1], asig[2])
		

	def bloques(self, bloque, table):
		bloque.pop(0)
		[*args] = bloque
		while bloque:
			x = bloque.pop(0) 
			if isinstance(x, list):
				if x[0] == 'declaracion_variables':
					self.declaraVariables(x, "local", table)
				if x[0] == 'estatutos':
					self.estatutos(x, table)
			if x == 'regresa':
				if bloque:
					self.quad(x, bloque.pop())
				else:
					self.quad(x)


	def declaraFunciones(self, table):
		dec_fun = self.dec_fun
		dec_fun = dec_fun.pop()
		
		# print(dec_fun)

		modulos = self.modulos(dec_fun)
		
		while modulos:
			modulo = modulos.pop(0)
			[*args] = modulo
			
			if len(args) == 4:

				modulot = args[0]
				tipo = args[1]
				nombre = args[2]
				argumentos = []
				funcSymbol = FunctionSymbol(nombre, tipo,argumentos)
				if not table.put(funcSymbol):
					print('Modulo '+ nombre+' already defined')
				funcionTable = SymbolTable(table, funcSymbol)
				self.quad("modulo", tipo, nombre)
				bloque = args[3]
				self.bloques(bloque, funcionTable)
			else:
				modulot = args[0]
				tipo = args[1]
				nombre = args[2]
				parametros = deepcopy(args[3])
				parametros2 = self.getParametros(parametros)
				bloque = args[4]
				funcSymbol = FunctionSymbol(nombre, tipo, parametros2)
				if not table.put(funcSymbol):
					print('Modulo'+ nombre+' already defined')
				funcionTable = SymbolTable(table, funcSymbol)
				self.quad("modulo", tipo, nombre)
				
				self.declaraVariables(args[3], "param",funcionTable.parent)
				self.bloques(bloque,funcionTable)

	def operacion(self, oper):
		cuadruploOP = []
		cuadruploOP.append(oper[1])
		cuadruploOP.append(oper[2])
		cuadruploOP.append(oper[3])
		return cuadruploOP		

	def quad(self,tipo, *args):
		cuadruplo = []
	
		if tipo == "programa":
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
		if tipo == "declaracion_variables":
			cuadruplo.append(args[1])
			cuadruplo.append(args[0])
			cuadruplo.append(args[2])
		if tipo == "modulo":
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
			cuadruplo.append(args[1])
		if tipo == "asignacion":
			
			if isinstance(args[1], list):
				cuadruploOP = self.operacion(args[1])

				cuadruplo.append("=")
				cuadruplo.append(args[0])
				cuadruplo.append(cuadruploOP)
				
			else:
				cuadruplo.append("=")
				cuadruplo.append(args[1])
				cuadruplo.append(args[0])
		if tipo == "si":
			cuadruploOP = self.operacion(args[0])
			cuadruplo.append(tipo)
			cuadruplo.append(cuadruploOP[0])
			cuadruplo.append(cuadruploOP[1])
			cuadruplo.append(cuadruploOP[2])
		if tipo == "sino":
			cuadruplo.append(tipo)
		if tipo == "mientras":
			cuadruploOP = self.operacion(args[0])
			cuadruplo.append(tipo)
			cuadruplo.append(cuadruploOP[0])
			cuadruplo.append(cuadruploOP[1])
			cuadruplo.append(cuadruploOP[2])
		if tipo == 'repite':
			cuadruplo.append(tipo)
		if tipo == "hasta":
			cuadruploOP = self.operacion(args[0])
			cuadruplo.append(tipo)
			cuadruplo.append(cuadruploOP[0])
			cuadruplo.append(cuadruploOP[1])
			cuadruplo.append(cuadruploOP[2])
		if tipo == 'end_control':
			cuadruplo.append(args[0])
		if tipo == 'llamada':
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
			
		if tipo == 'parametros':
			cuadruplo.append("param")
			cuadruplo.append(args[0])
		if tipo == 'regresa':
			cuadruplo.append(tipo)
			if args:
				cuadruplo.append(args[0])
		if tipo == 'principal':
			cuadruplo.append(tipo)
			cuadruplo.append(tipo)

		
		json.dump(cuadruplo, file)
		file.write(",")
		file.write("\n")


		
		

		