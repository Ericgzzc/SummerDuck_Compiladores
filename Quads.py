from Var_Table import *
from cubo import *
import json 
import sys

class Quads(object):
	global file 	
	file = open("CodigoIntermedio.txt", "w")

	def __init__(self,tree):
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
		self.declaraVariables(self.dec_val, "global")
		self.declaraFunciones()
		self.metodo_principal(principal)

	def metodo_principal(self,principal):
		
		principal_nomb, *args = principal
		
		self.quad(principal_nomb)
		if len(args) == 2:
			self.declaraVariables(args[0], principal_nomb)
			self.estatutos(args[1])
		else:
			if args[0][0] == 'declaracion_variables':
				self.declaraVariables(args[0], principal_nomb)
			else:
				self.estatutos(args[0])
		
	def declaraVariables(self,dec_val,var_tipo):
		if dec_val:
			while dec_val[1]:
				tipo = dec_val[1].pop(0)
				variables = dec_val[1].pop(0)
				for x in variables:
					self.quad("declaracion_variable", tipo,var_tipo, x)
					

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
	def estatutos(self, estatutos):
		estatutos.pop(0)
		while estatutos[0]:
			x = estatutos[0].pop(0)
			if x[0] == 'asignacion':
				self.asignacion(x)
			if x[0] == 'decision':
				self.decision(x)
			if x[0] == 'repeticion':
				y = x.pop(1)
				if y[0]=='mientras':
					self.mientras(y)
				if y[0]=='repite':
					self.repite(y)
			if x[0] == 'llamada':
				self.llamada(x)
			if x[0] == 'lectura':
				self.lectura(x)
			if x[0] == 'escritura':
				self.escritura(x)

	def escritura(self, llam):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def lectura(self, llam):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def llamada(self, llam):
		self.quad(llam[0], llam[1], llam[2])
		for x in llam[2]:
			self.quad("parametros", x)

	def repite(self,rep):		
		repite, hacer, exp = rep
		hacer = hacer.pop()
		self.quad(repite)
		self.estatutos(hacer)
		self.quad("hasta", exp)
	
	def mientras(self,whil):
		mientras, exp, hacer = whil
		self.quad(mientras, exp)
		hacer = hacer.pop()
		self.estatutos(hacer)
		self.quad("end_control", "end_mientras")

	def decision(self, dec):
		dec.pop(0)
		if len(dec) == 3:
			si, exp, hacer = dec
			self.quad(si, exp)
			hacer = hacer.pop()
			self.estatutos(hacer)
			self.quad("end_control", "end_si")
		else:
			si, exp, hacer, sino, hacer2 = dec
			self.quad(si, exp)
			hacer = hacer.pop()
			self.estatutos(hacer)
			self.quad(sino,)
			hacer2 = hacer2.pop()
			self.estatutos(hacer2)
			self.quad("end_control", "end_sino")
			self.quad("end_control", "end_si")
		
		
			
	def asignacion(self, asig):
		self.quad(asig[0], asig[1], asig[2])

	def bloques(self, bloque):
		bloque.pop(0)
		[*args] = bloque
		while bloque:
			x = bloque.pop(0) 
			if isinstance(x, list):
				if x[0] == 'declaracion_variables':
					self.declaraVariables(x, "local")
				if x[0] == 'estatutos':
					self.estatutos(x)
			if x == 'regresa':
				if bloque:
					self.quad(x, bloque.pop())
				else:
					self.quad(x)


	def declaraFunciones(self):
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
				self.quad("modulo", tipo, nombre)
				bloque = args[3]
				self.bloques(bloque)
			else:
				modulot = args[0]
				tipo = args[1]
				nombre = args[2]
				parametros = args[3]
				self.quad("modulo", tipo, nombre)
				self.declaraVariables(parametros, "param")
				bloque = args[4]
				self.bloques(bloque)
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
		if tipo == "declaracion_variable":
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
				cuadruplo.append(cuadruploOP)
				cuadruplo.append(args[0])
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


		
		

		