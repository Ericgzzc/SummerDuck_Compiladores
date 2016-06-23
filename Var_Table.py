
# entero 		0 - 5000
# real 	 		5001 - 10000
# char 			10001 - 15000


class tablaVars(dict):

	def __init__(self, enteroPointer = 0, realPointer = 5001, charPointer = 10000):
		self.enteroPointer = enteroPointer  		
		self.realPointer = realPointer 	
		self.charPointer = charPointer 		
		self.temp = 0
		self.lastpointer = 0

	def getEnteroPointer(self):
		return self.enteroPointer

	def getRealPointer(self):
		return self.realPointer

	def getCharPointer(self):
		return self.charPointer

	def getlastpointer(self):
		return self.lastpointer

	def add(self, scope, tipo, nombre):
		
		# Agrega alcance de la variable
		if scope not in self:
			self[scope] = {}

		# Agrega el tipo de la variable
		if tipo not in self[scope]:
			self[scope][tipo] = {}


		if nombre is "temp":
			nombre = "t" + str(self.temp)
			self.temp += 1

		# Checa si la variable ya esta agregada y la regresa
		if nombre in self[scope][tipo]:
			return self[scope][tipo][nombre]

		if tipo == 'entero':
			self[scope][tipo][nombre] = self.enteroPointer
			self.lastpointer = self.enteroPointer
			self.enteroPointer += 1

		elif tipo == 'real':
			self[scope][tipo][nombre] = self.realPointer
			self.lastpointer = self.realPointer
			self.realPointer += 1

		elif tipo == 'char':
			self[scope][tipo][nombre] = self.charPointer
			self.lastPointer = self.charPointer
			self.charPointer += 1
		
#Falta agregar funciones.

		else:
			raise Exception("No type")

		return self.lastpointer

globaltable = tablaVars()
globaltable.add('global', 'entero', 20)
globaltable.add('global', 'entero', 'a')
globaltable.add('local', 'entero', 'b')
globaltable.add('local', 'real', 'real')
globaltable.add('local', 'real', 'real')
globaltable.add('local', 'char', 'aaa')
print (globaltable.items())

