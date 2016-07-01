from Symboltable import *
from cubo import *
import numbers
import json 
import sys
import re
from copy import deepcopy
from arbolExpresion import*

class Quads(object):
	global file 
	global filename
	filename = "codigoIntermedio.txt"
	file = open(filename, "w")
	file.close()
	

	def __init__(self,tree):
		self.symbolTable = SymbolTable(None, 'global')
		self.arbol = tree
		self.PC = 1
		self.LBL = 1
		programa, nombre, *args, principal = self.arbol;
		self.programa = programa
		self.nombre = nombre
		self.principal = principal
		self.error = True
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
						print (var_tipo + '  '+ x+'   alreday declared in  '+ table.name)
						self.error = False
					self.quad("declaracion_variables", tipo,var_tipo, x)
		

	def getParametros(self,dec_val):
		param = []
		parame = dec_val
		tipoLista = []
		if parame:
			while parame[1]:
				tipo = parame[1].pop(0)
				variables = parame[1].pop(0)
				for x in variables:
					tipoLista = tipoLista + [tipo,]
					param = param + [x,]
		return [param,tipoLista]

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
		estatuto = estatutos.pop()
		while estatuto:
			x = estatuto.pop(0)
			print("estatuto",x)
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
				self.PC+=1
				self.llamada(x,table)
			if x[0] == 'lectura':
				self.lectura(x,table)
			if x[0] == 'escritura':
				self.escritura(x, table)

	def escritura(self, llam,table):
		self.quad(llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def lectura(self, llam,table):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def existenVariables(self, param, table):
		print("here1")

	def checkExp(self, arg):
		if "+" in arg or "-" in arg or "*" in arg or "/" in arg:
			return(True)
		else: 
			return(False)

	def llamada(self, llam, table):
		symbol = table.get(llam[1])
		exp = False;
		if isinstance(symbol, FunctionSymbol):
			if len(symbol.arguments) != len(llam[2]):
				self.error = False
				print('Llamada  ' + llam[1] + '  expected '+ str(len(symbol.arguments)) + ' arguments')
			else:	
				exptectedTypes = symbol.tipoVariables
				types = []
				
				if isinstance(llam[2], list):
					
					for arg in llam[2]:
						if self.checkExp(arg):
							pass
						else:
							if table.get(arg):
								types = types + [table.get(arg).type,]
							else:
								self.error = False
								print('Variable  ' + arg + '  No declaraded')
				
				if len(exptectedTypes) == len(types):
					for exprType, expectedType, i in zip(types, exptectedTypes,range(1, len(types) + 1)):
						if exprType != expectedType and not (exprType == 'entero' and expectedType == 'real'):
							self.error = False
							print ('Incorrect type of parameter, expected '+expectedType+", found "+exprType + " in "+ llam[1])
		if symbol == None:
			self.error = False
			print('modulo  ' + llam[1] + '  No declared' )
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			if self.checkExp(x):
				param = self.operaciones(x,table)
				self.quad("parametros", param)
			else:
				self.quad("parametros", x)
		self.PC+=1
		self.quad("goto",self.getVariableTemporal(), self.getLabel())
		

	def getVariableTemporal(self):
		return("t"+str(self.PC))

	def getLabel(self):
		
		return("label"+str(self.LBL))

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

		if len(dec) == 4:
			tipo, si, exp, hacer = dec
			varif=self.operaciones(exp, table)
			self.LBL+=1
			hacerx = hacer.pop()
			print("deci", hacerx)
			self.quad("si", varif, self.getLabel())
			self.estatutos(hacerx, table)
			# self.quad("end_control", "end_si")
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

	def imprimirError(self,resultado, a, b, op):
		if resultado != 'Error':
				return(resultado)
		else:
				self.error = False
				print("Cant do operation  " + str(a) + " " + str(op) + " " + str(b)+ "  incompatyble types")
				return("Error")
		
	def checarOperacion(self,a,b,op, table):
		operando1 = table.get(a)
		operando2 = table.get(b)
		

		if operando1 != None and operando2 != None:
			result = cubo[operando1.type][operando2.type][op]
			return(self.imprimirError(result, a, b, op))
		elif operando1 == None and operando2 == None:
				if isinstance(b, int) and isinstance(a, int):
					result = cubo["entero"]["entero"][op]
					return(self.imprimirError(result, a, b, op))
				elif isinstance(b, float) and isinstance(a, float):
					result = cubo["real"]["real"][op]
					return(self.imprimirError(result, a, b, op))
				elif isinstance(b, int) and isinstance(a, float):
					result = cubo["real"]["entero"][op]
					return(self.imprimirError(result, a, b, op))
				elif isinstance(b, float) and isinstance(a, int):
					result = cubo["entero"]["real"][op]
					return(self.imprimirError(result, a, b, op))
				else:
					self.error = False
					print("Variable  " + str(b)  + "  No declared")
					return("Error")
		elif operando1 == None:
				if isinstance(a, int):
					result = cubo["entero"][operando2.type][op]
					return(self.imprimirError(result, a, b, op))
				elif isinstance(a, float):
					result = cubo["real"][operando2.type][op]
					return(self.imprimirError(result, a, b, op))
				else:
					self.error = False
					print("Variable  " + str(a) + "  No declared")
					return("Error")
		elif operando2 == None:

				if isinstance(b, int):
					result = cubo["entero"][operando1.type][op]
					return(self.imprimirError(result, a, b, op))
				elif isinstance(b, float):
					result = cubo["real"][operando1.type][op]
					return(self.imprimirError(result, a, b, op))
				else:
					self.error = False
					print("Variable  " + str(b) + "  No declared")
					return("Error")

	def meterLista(self, a, lista, table, stackNumeros, stackOperando):
		print("meter", stackNumeros)
		print("meter", stackOperando)
		print("\n")
		if a == "*" or a == "/":
			stackOperando.append(a)
		elif a == "<" or a == ">"or a == "==":
			stackOperando.append(a)
		elif a == "+" or a == "-":
			if self.checarTopFactor(stackOperando):
				self.PC+=1
				operando2 = stackNumeros.pop()
				operando1 = stackNumeros.pop()
				operacion = stackOperando.pop()
				res = self.makeQuadruplo(operacion, operando2, operando1)
				stackNumeros.append(res)
			if self.checarTopTermino(stackOperando):
				self.PC+=1
				operando2 = stackNumeros.pop()
				operando1 = stackNumeros.pop()
				operacion = stackOperando.pop()
				res = self.makeQuadruplo(operacion, operando2, operando1)
				stackNumeros.append(res)

			stackOperando.append(a)
		else: 
			stackNumeros.append(a)


	def checarTopFactor(self, stackOperando):
		if stackOperando:
			if stackOperando[-1] == "*" or stackOperando[-1] == "/":
				return(True)
		else:
			return(False)
	def checarCondicion(self, stackOperando):
		if stackOperando:
			if stackOperando[-1] == "<" or stackOperando[-1] == ">" or stackOperando[-1] == "==":
				return(True)
		else:
			return(False)
	def checarTopTermino(self, stackOperando):
		if stackOperando:
			if stackOperando[-1] == "-" or stackOperando[-1] == "+":
				return(True)
		else:
			return(False)
	def makeQuadruplo(self, operacion, operando1, operando2):
		vartemp = self.getVariableTemporal()
		self.quad("operacion", operacion, operando2, operando1, vartemp)
		return vartemp

	def operaciones(self, oper, table):
		stackNumeros = []
		stackOperando = []
		mv = arbolExpresion(oper)
		lista = mv.expression()
		# lista = self.makeList(arbol)
		print(lista)
		while lista:
			a = lista.pop(0)
			self.meterLista(a, lista, table, stackNumeros, stackOperando)

		if not lista:
			if self.checarTopTermino(stackOperando):
				self.PC+=1
				operando2 = stackNumeros.pop()
				operando1 = stackNumeros.pop()
				operacion = stackOperando.pop()
				res = self.makeQuadruplo(operacion, operando2, operando1)
				stackNumeros.append(res)
			if self.checarTopFactor(stackOperando):
				self.PC+=1
				operando2 = stackNumeros.pop()
				operando1 = stackNumeros.pop()
				operacion = stackOperando.pop()
				res = self.makeQuadruplo(operacion, operando2, operando1)
				stackNumeros.append(res)
			if self.checarCondicion(stackOperando):
				self.PC+=1
				operando2 = stackNumeros.pop()
				operando1 = stackNumeros.pop()
				operacion = stackOperando.pop()
				res = self.makeQuadruplo(operacion, operando2, operando1)
				stackNumeros.append(res)
		return stackNumeros.pop()
			

	# def makeList(self, aNode, a = []):
		
	# 	if aNode:
	# 		self.makeList(aNode.left, a)
	# 		a.append(aNode.data)
	# 		self.makeList(aNode.right, a)
	# 	return a

	def asignacion(self, asig, table):
		resultado = ""
		a = table.get(asig[1]);
		llamada = False
		exp = False
		if a == None:
			pass
		else:
			if isinstance(asig[2], list):
				if asig[2][0] == "llamada":
					llamada = True
					self.llamada(asig[2],table)
					resultado = a.type
			elif table.get(asig[2]):
				var = table.get(asig[2]);
				if var != None:
					resultado = cubo[var.type][a.type]["="]						
			
			elif isinstance(asig[2], int):
					resultado = cubo["entero"][a.type]["="]
			elif isinstance(asig[2], float):
					resultado = cubo["real"][a.type]["="]
			elif self.checkExp(asig[2]):
					exp = True
					res = self.operaciones(asig[2], table)
					
					resultado = a.type
			else:
					resultado = cubo["char"][a.type]["="]

		if resultado != a.type:

			self.error = False
			print("Cant assign incomptyble types  " + str(a.name) + " exptected " + str(a.type) + " given " + str(resultado))		
		if llamada:
			self.quad(asig[0], asig[1], self.getVariableTemporal())
		elif exp:
			self.quad(asig[0], asig[1], res)
		else:
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
					a = bloque.pop()

					var = table.get(a)
					if var != None:
						table2 = table.parent.get(table.name)
						if table2.type != var.type:
							if table2.type == "void":
								self.error = False
								print("Modulo " +table2.name + " is not expecting a return variable, type is void" )
							else:
								self.error = False
								print('return variable ' + a + '  has a different type, expected ' + table2.type + " given " + var.type + " in modulo "+ table2.name)
					else:
						self.error = False
						print('Variable  ' + a + '  No declared')
					self.quad(x, a)
				else:
					table2 = table.parent.get(table.name)
					if table2.type != "void":
						self.error = False
						print("Modulo " +table2.name + " is expecting a return variable")

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
				funcSymbol = FunctionSymbol(nombre, tipo,argumentos,argumentos)
				if not table.put(funcSymbol):
					self.error = False
					print('Modulo '+ nombre+' already defined')
				funcionTable = SymbolTable(table, nombre)
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
				funcSymbol = FunctionSymbol(nombre, tipo, parametros2[0], parametros2[1])
				if not table.put(funcSymbol):
					self.error = False
					print('Modulo'+ nombre+' already defined')
				funcionTable = SymbolTable(table, nombre)
				self.quad("modulo", tipo, nombre)
				
				self.declaraVariables(args[3], "param",funcionTable)
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
		
				cuadruplo.append("=")
				cuadruplo.append(args[0])
				cuadruplo.append(args[1])

		if tipo == "si":
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
			cuadruplo.append(args[1])
		if tipo == "sino":
			cuadruplo.append(tipo)
		if tipo == "mientras":
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
		if tipo == 'repite':
			cuadruplo.append(tipo)
		if tipo == "hasta":
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
		if tipo == 'end_control':
			cuadruplo.append(args[0])
		if tipo == 'lectura':
			cuadruplo.append("lee")
		if tipo == 'escribe':
			cuadruplo.append(tipo)
		if tipo == 'llamada':
			cuadruplo.append(tipo)
			cuadruplo.append(args[0])
		if tipo == 'parametros':
			cuadruplo.append("param")
			cuadruplo.append(args[0])
		if tipo == 'goto':
			cuadruplo.append("goto")
			cuadruplo.append(args[0])
		if tipo == 'regresa':
			cuadruplo.append(tipo)
			if args:
				cuadruplo.append(args[0])
		if tipo == 'principal':
			cuadruplo.append(tipo)
			cuadruplo.append(tipo)
		if tipo == "operacion":
			cuadruplo.append(args[0])
			cuadruplo.append(args[1])
			cuadruplo.append(args[2])
			cuadruplo.append(args[3])

		file = open(filename, "a")
		
		json.dump(cuadruplo, file)

		file.write("\n")
		file.close()


		
		

		