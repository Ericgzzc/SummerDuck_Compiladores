from Var_Table import *
from cubo import *
import sys

class Quads(object):


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
		# self.declaraVariables()

	
		
	def declaraVariables(self):
		print(self.dec_val)
		# print(self.dec_val[1])
		# print(len(self.dec_val))
		# for items in self.dec_val[1]:
		# 	print(items)
		
	



		
		

		