

from VarTable import *
from cubo import *
import sys
Matricial = []
Temporal = 0

Avail = []		# Pila de temporales
globaltable = tablaVars() # (entero -> 0), (real -> 5001), (char -> 10000), 

#						entero  real  char    bin    hex
localtable = tablaVars(25001, 30001, 45001)

#							 entero   real  char
tablaTemporales = tablaVars(70001, 85000, 90000)
file = open("CodigoFinal.txt", "w")
file.write("#include <Servo.h>")
file.write("#include <math.h>")
file.write("\n")
file.write("\n")

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

def fun(tipo, *args):
	operador = []
cuadruplo = []
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


def fun(tipo, *args):
	global cont
	global PC
	global notPopedYet
	global HERE
	global cuadruplo
#	print ('A is: ', tipo)
#	print ('ARGS: ', args)
	notPopedYet=True
	if tipo == 'SUBVARS':
		cuadruplo.append("=")
		cuadruplo.append(args[1])
		cuadruplo.append(args[2])
		PC += 1

	elif tipo == 'SUBVARS2':
		cuadruplo.append("asignar")
		cuadruplo.append(args[0])
		cuadruplo.append(args[1])
		PC += 1
		
	elif tipo == 'SINTAXESPECIAL':
		cuadruplo.append(args[0])
		cuadruplo.append(args[1])

	elif tipo == 'SINTAXESPECIAL3':
		cuadruplo.append(args[0])
		cuadruplo.append(args[1])
		cuadruplo.append(args[2])


	elif tipo == 'STARTVOIDS':
		cuadruplo.append('INICIANVOIDS')
		cuadruplo.append(args[0])
		

	elif tipo == 'SINTAXESPECIAL2':
		cuadruplo.append(args[0])

	#elif tipo == 'DEFINICIONES':
		

	elif tipo == 'WHILE':
		HERE -= 1
		cuadruplo.append('WHILE')
		HERE += 1
		cuadruplo.append(HERE)

	elif tipo == 'IF':
		cuadruplo.append('IF')
		HERE += 1

	elif tipo == 'VOID':
		cuadruplo.append('VOID')
		cuadruplo.append(args[0])
		HERE += 1
		cuadruplo.append(args[1])
		HERE += 1
		cuadruplo.append(args[2])
		HERE += 1

	elif tipo == 'LLAMARVOIDPARAM':
		cuadruplo.append('LLAMARVOIDPARAM')
		cuadruplo.append(args[0])
		HERE += 1
		cuadruplo.append(args[1])
		HERE += 1
		cuadruplo.append(args[2])
		HERE += 1

	elif tipo == 'LLAMARVOID':
		cuadruplo.append('LLAMARVOID')
		cuadruplo.append(args[0])
		HERE += 1
		cuadruplo.append(args[1])
		HERE += 1

	elif tipo == 'DEFINIR':
		cuadruplo.append('DEFINIR')
		HERE += 1

	elif tipo == 'VOIDPARAM':
		cuadruplo.append('VOIDPARAM')
		cuadruplo.append(args[0])
		HERE += 1
		cuadruplo.append(args[1])
		HERE += 1
		cuadruplo.append(args[2])
		HERE += 1
		cuadruplo.append(args[3])
		HERE += 1

	elif tipo == 'LLAMADAFUNCT':
		cuadruplo.append('LLAMADAFUNCT')
		cuadruplo.append(args[1])
		cuadruplo.append(args[2])

	elif tipo == 'ASIGNAR':
		Operador = args[0]
		if args[2] == None:
			Operando2 = args[1]
			Operando1 = pilaO.pop()
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)

		else:
			Operador = args[0]
			Operando2 = args[1]
			Operando1 = args[2]
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)

	elif tipo == 'ASIGNAR2':
		cuadruplo.append(args[0])
		cuadruplo.append(args[1])
		cuadruplo.append(args[2])
		cuadruplo.append(args[3])

	elif tipo == 'RELOP':
		Operador = args[0]
		Operando1 = args[1]
		Operando2 = args[2]
		cuadruplo.append(Operador)
		cuadruplo.append(Operando1)
		cuadruplo.append(Operando2)
#		cuadruplo.append('ResRELOP')
		cuadruplo.append('gotoF HERE')
		pilaO.append('ResRELOP')

	elif tipo == 'TIMDIV':
		Operador = args[0]
		if args[1] == None and args[2] != None:
			Operando1 = pilaO.pop()
			Operando2 = args[2]
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResTIMDIV')
			pilaO.append('ResTIMDIV')

		elif args[1] == None and args[2] == None:
			Operando1 = pilaO.pop()
			Operando2 = pilaO.pop() 
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResTIMDIV')
			pilaO.append('ResTIMDIV')

		else:
			Operador = args[0]
			Operando1 = args[1]
			Operando2 = args[2]
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResTIMDIV')
			pilaO.append('ResTIMDIV')

	elif tipo == 'PLUSMINUS':
		Operador = args[0]
		if args[1] == None and args[2] != None:
			Operando1 = pilaO.pop()
			Operando2 = args[2]
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResPLUSMINUS')
			pilaO.append('ResPLUSMINUS')

		elif args[1] == None and args[2] == None:
			Operando1 = pilaO.pop()
			Operando2 = pilaO.pop() 
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResPLUSMINUS')
			pilaO.append('ResPLUSMINUS')

		else:
			Operador = args[0]
			Operando1 = args[1]
			Operando2 = args[2]
			cuadruplo.append(Operador)
			cuadruplo.append(Operando1)
			cuadruplo.append(Operando2)
			cuadruplo.append('ResPLUSMINUS')
			pilaO.append('ResPLUSMINUS')

	elif tipo == 'LOOP':
		cuadruplo.append('goto LOOP')

	elif tipo == 'AJUSTE':
		cuadruplo.append(args[0])

	elif tipo == 'INICIAR':
		cuadruplo.append('LOOP:')

	elif tipo == 'END':
		cuadruplo.append('END')
#		print(cuadruplo)
#		PC.append(cont)
#		num = 0
#		file = open("TextSalida.txt", "w")
#		file = open("Ensamblador.txt", "w")
		
#		file.write(str(cuadruplo))

		
		cuadruplo.reverse()
		print(cuadruplo)
		
		if notPopedYet :
			Evaluar = cuadruplo.pop()
		
		notPopedYet=True
		BandCond = False
		FuncionDeclarada = False 
		while (Evaluar != 'END'):

			# ----------- Asignacion-------------------------#
			if Evaluar == '=':
			    Variable1 = cuadruplo.pop() # 255
			    Asignacion = cuadruplo.pop() # uterre

			    if BandCond == True or FuncionDeclarada == True:
			    	#if (Variable1 == 'LeerDig'):
			    	#	file.write(str(Asignacion))
			    	#	file.write(" = ")
			    	#	file.write("digitalRead(")
			    	#	Asignacion = cuadruplo.pop()
			    	#	file.write(str(Asignacion))
			    	#	file.write(");")
			    	#	file.write("\n")

			    	#elif (Variable1 == 'ResPLUSMINUS' or Variable1 == 'ResTIMDIV'):
			    	#	SumaResta.append('TerminaPUUUUM')
			    	#	SumaResta.reverse()
			    	#	file.write(str(Asignacion))
			    	#	file.write(" =")
			    	#	Resultado = SumaResta.pop()

			    	#	while (Resultado != 'TerminaPUUUUM'):
			    	#		file.write(" ")
			    	#		file.write(str(Resultado))
			    	#		Resultado = SumaResta.pop()

			    	#	file.write(";")
			    	#	file.write("\n")

			    	Condicional.append(Evaluar)
			    	Condicional.append(Variable1)
			    	Condicional.append(Asignacion)


			    	#elif (isinstance(Asignacion, int)):
			    	#	file.write("int ")
			    	#	file.write(str(Variable1))
			    	#	file.write(" = ")
			    	#	file.write(str(Asignacion))
			    	#	file.write(";")
			    	#	file.write("\n")

			    else:
			    	if (Variable1 == 'LeerDig'):
			    		file.write(str(Asignacion))
			    		file.write(" = ")
			    		file.write("digitalRead(")
			    		Asignacion = cuadruplo.pop()
			    		file.write(str(Asignacion))
			    		file.write(");")
			    		file.write("\n")

			    	elif (Variable1 == 'ResPLUSMINUS' or Variable1 == 'ResTIMDIV'):
			    		SumaResta.append('TerminaPUUUUM')
			    		SumaResta.reverse()
			    		file.write(str(Asignacion))
			    		file.write(" =")
			    		Resultado = SumaResta.pop()

			    		while (Resultado != 'TerminaPUUUUM'):
			    			file.write(" ")
			    			file.write(str(Resultado))
			    			Resultado = SumaResta.pop()

			    		file.write(";")
			    		file.write("\n")

			    	elif (isinstance(Asignacion, int)):
			    		file.write("int ")
			    		file.write(str(Variable1))
			    		file.write(" = ")
			    		file.write(str(Asignacion))
			    		file.write(";")
			    		file.write("\n")

			    	elif (isinstance(Asignacion, float)):
			    		file.write("double ")
			    		file.write(str(Variable1))
			    		file.write(" = ")
			    		file.write(str(Asignacion))
			    		file.write(";")
			    		file.write("\n")

			#-----------------Suma y Resta-----------------------------#
			elif Evaluar == '+' or Evaluar == '-':
				PrimOp = cuadruplo.pop()
				SegOp = cuadruplo.pop()
				TerOp = cuadruplo.pop()

				if BandCond == True or FuncionDeclarada == True:
					Condicional.append(Evaluar)
					Condicional.append(PrimOp)
					Condicional.append(SegOp)
					Condicional.append(TerOp)
					
				else:
					if (PrimOp != 'ResPLUSMINUS' and PrimOp != 'ResTIMDIV'):
						SumaResta.append(PrimOp)
						SumaResta.append(Evaluar)
						SumaResta.append(SegOp)
					else:
						SumaResta.append(Evaluar)
						SumaResta.append(SegOp)

			#-----------------Suma y Resta-----------------------------#
			elif Evaluar == '*' or Evaluar == '/':
				PrimOp = cuadruplo.pop()
				SegOp = cuadruplo.pop()
				TerOp = cuadruplo.pop()

				if BandCond == True or FuncionDeclarada == True:
					Condicional.append(Evaluar)
					Condicional.append(PrimOp)
					Condicional.append(SegOp)
					Condicional.append(TerOp)

				else:
					if (PrimOp != 'ResTIMDIV'):
						SumaResta.append(PrimOp)
						SumaResta.append(Evaluar)
						SumaResta.append(SegOp)
					else:
						SumaResta.append(Evaluar)
						SumaResta.append(SegOp)


			#------------Definir funciones-----------------------------
			elif Evaluar == 'INICIANVOIDS':
				file.write("void ")
				Evaluar = cuadruplo.pop()
				file.write(str(Evaluar))
				file.write("(){")
				file.write("\n")


			#-----------------Comparadores-----------------------------#
			elif Evaluar == '==' or Evaluar == '<' or Evaluar == '>' or Evaluar == '<=' or Evaluar == '>=' or Evaluar == 'true' or Evaluar == 'false' or Evaluar == 'AND' or Evaluar == 'OR' or Evaluar == 'NE':
				PrimOp = cuadruplo.pop()
				SegOp = cuadruplo.pop()
				TerOp = cuadruplo.pop()
				Condicional.append(Evaluar)
				Condicional.append(PrimOp)
				Condicional.append(SegOp)
				Condicional.append(TerOp)
				if TerOp == 'gotoF HERE':
					Condicional.append('){')
					BandCond = True

			#-----------------IF-----------------------------#
			elif Evaluar == 'IF' or Evaluar == 'WHILE' or Evaluar == 'VOID':
				Condicional.append('TerminaPUUUUM')
				Condicional.reverse()

				if Evaluar == 'IF':
					file.write("if ")
					

				elif Evaluar == 'WHILE':
						
					 file.write("while ")

				elif Evaluar == 'void':
					file.write("void ")
					Evaluar = Condicional.pop()
					Evaluar = Condicional.pop()
					file.write(Evaluar)
					file.write("(){")
					file.write("\n")

				EvaluarCond = Condicional.pop()
				while EvaluarCond != 'TerminaPUUUUM':

					if EvaluarCond == '==' or EvaluarCond == '<' or EvaluarCond == '>' or EvaluarCond == '<=' or EvaluarCond == '>=' or EvaluarCond == 'true' or EvaluarCond == 'false' or EvaluarCond == 'AND' or EvaluarCond == 'OR' or EvaluarCond == 'NE':
						PrimOp = Condicional.pop()
						SegOp = Condicional.pop()
						TerOp = Condicional.pop()
						file.write("(")
						file.write(str(PrimOp)) 
						
						if EvaluarCond == 'AND':
							file.write(" && ")
						elif EvaluarCond == 'OR':
							file.write(" || ")
						else:
							file.write(str(EvaluarCond))
		
						file.write(str(SegOp))

						if (TerOp == 'gotoF HERE'):
							file.write("){")
							file.write("\n")

					elif EvaluarCond == 'Atras':
						file.write("digitalWrite(2, LOW);")
						file.write("\n")
						file.write("digitalWrite(3, HIGH);")
						file.write("\n")
						file.write("digitalWrite(4, LOW);")
						file.write("\n")
						file.write("digitalWrite(5, HIGH);")
						file.write("\n")
						file.write("delay(1000);")
						file.write("\n")

					elif EvaluarCond== 'print':
						file.write("Serial.println(")
						file.write(str(Variable1))
						file.write(");")
						file.write("\n")

					elif EvaluarCond == 'Adelante':
						file.write("digitalWrite(2, HIGH);")
						file.write("\n")
						file.write("digitalWrite(3, LOW);")
						file.write("\n")
						file.write("digitalWrite(4, HIGH);")
						file.write("\n")
						file.write("digitalWrite(5, LOW);")
						file.write("\n")
						file.write("delay(1000);")
						file.write("\n")

					elif EvaluarCond == 'retraso':
							file.write("delay(")
							file.write(str(Variable1))
							file.write(");")
							file.write("\n")

					elif EvaluarCond == 'Escribir':
						if Asignacion == 'high':
							file.write("digitalWrite(")
							file.write(Variable1)
							file.write(", HIGH);")
							file.write("\n")

						elif Asignacion == 'low':
							file.write("digitalWrite(")
							file.write(Variable1)
							file.write(", LOW);")
							file.write("\n")

					elif EvaluarCond== 'Izquierda':
						file.write("digitalWrite(2, LOW);")
						file.write("\n")
						file.write("digitalWrite(3, LOW;")
						file.write("\n")
						file.write("digitalWrite(4, HIGH);")
						file.write("\n")
						file.write("digitalWrite(5, LOW);")
						file.write("\n")

					elif EvaluarCond== 'Derecha':
						file.write("digitalWrite(2, HIGH);")
						file.write("\n")
						file.write("digitalWrite(3, LOW;")
						file.write("\n")
						file.write("digitalWrite(4, LOW);")
						file.write("\n")
						file.write("digitalWrite(5, LOW);")
						file.write("\n")

					elif EvaluarCond== 'Apagar':
						file.write("digitalWrite(2, LOW);")
						file.write("\n")
						file.write("digitalWrite(3, LOW);")
						file.write("\n")
						file.write("digitalWrite(4, LOW);")
						file.write("\n")
						file.write("digitalWrite(5, LOW);")
						file.write("\n")
						file.write("delay(1000000);")
						file.write("\n")


					elif EvaluarCond == '=':
						Variable1 = Condicional.pop() # 255
						Asignacion = Condicional.pop()

						if (Variable1 == 'LeerDig'):
							file.write(str(Asignacion))
							file.write(" = ")
							file.write("digitalRead(")
							Asignacion = Condicional.pop()
							file.write(str(Asignacion))
							file.write(");")
							file.write("\n")

						elif (Variable1 == 'ResPLUSMINUS' or Variable1 == 'ResTIMDIV'):
							CondSumaResta.append('TerminaPUUUUM')
							CondSumaResta.reverse()
							file.write(str(Asignacion))
							file.write(" =")
							Resultado = CondSumaResta.pop()

							while (Resultado != 'TerminaPUUUUM'):
								file.write(" ")
								file.write(str(Resultado))
								Resultado = CondSumaResta.pop()

							file.write(";")
							file.write("\n")

						elif (isinstance(Asignacion, int)):
							file.write("int ")
							file.write(str(Variable1))
							file.write(" = ")
							file.write(str(Asignacion))
							file.write(";")
							file.write("\n")

						elif (isinstance(Variable1, int)):
							file.write(str(Asignacion))
							file.write(str(EvaluarCond))
							file.write(str(Variable1))
							file.write(";")
							file.write("\n")


					elif EvaluarCond == '*' or EvaluarCond == '/':
						PrimOp = Condicional.pop()
						SegOp = Condicional.pop()
						TerOp = Condicional.pop()

						if (PrimOp != 'ResTIMDIV'):
							CondSumaResta.append(PrimOp)
							CondSumaResta.append(EvaluarCond)
							CondSumaResta.append(SegOp)
						
						else:
							CondSumaResta.append(EvaluarCond)
							CondSumaResta.append(SegOp)

					elif EvaluarCond == '+' or EvaluarCond == '-':
						PrimOp = Condicional.pop()
						SegOp = Condicional.pop()
						TerOp = Condicional.pop()

						if (PrimOp != 'ResPLUSMINUS'):
							CondSumaResta.append(PrimOp)
							CondSumaResta.append(EvaluarCond)
							CondSumaResta.append(SegOp)
						
						else:
							CondSumaResta.append(EvaluarCond)
							CondSumaResta.append(SegOp)

					EvaluarCond = Condicional.pop()
					BandCond = False
					FuncionDeclarada = False

				file.write("}")
				file.write("\n")






			#	file.write(str(Variable1))
			#	file.write(" = ")
			#	file.write(str(Asignacion))
			#	file.write(";")
			#	file.write("\n")

			elif Evaluar == 'LLAMARVOID':
				Evaluar = cuadruplo.pop()
				Evaluar = cuadruplo.pop()
				file.write(str(Evaluar))
				file.write("();")
				file.write("\n")


			elif Evaluar == 'Adelante':
				if BandCond == True:
					Condicional.append(Evaluar)

				else:
					file.write("digitalWrite(2, HIGH);")
					file.write("\n")
					file.write("digitalWrite(3, LOW);")
					file.write("\n")
					file.write("digitalWrite(4, HIGH);")
					file.write("\n")
					file.write("digitalWrite(5, LOW);")
					file.write("\n")
					file.write("delay(1000);")
					file.write("\n")
			elif Evaluar == 'Derecha':
				if BandCond == True:
					Condicional.append(Evaluar)
				else:
					file.write("digitalWrite(2, HIGH);")
					file.write("\n")
					file.write("digitalWrite(3, LOW);")
					file.write("\n")
					file.write("digitalWrite(4, LOW);")
					file.write("\n")
					file.write("digitalWrite(5, LOW);")
					file.write("\n")

			elif Evaluar == 'Izquierda':
				if BandCond == True:
					Condicional.append(Evaluar)
				else:
					file.write("digitalWrite(2, LOW);")
					file.write("\n")
					file.write("digitalWrite(3, LOW);")
					file.write("\n")
					file.write("digitalWrite(4, HIGH);")
					file.write("\n")
					file.write("digitalWrite(5, LOW);")
					file.write("\n")

			elif Evaluar == 'Apagar':
				if BandCond == True:
					Condicional.append(Evaluar)
				else:
					file.write("digitalWrite(2, LOW);")
					file.write("\n")
					file.write("digitalWrite(3, LOW);")
					file.write("\n")
					file.write("digitalWrite(4, LOW);")
					file.write("\n")
					file.write("digitalWrite(5, LOW);")
					file.write("\n")
					file.write("delay(10000);")
					file.write("\n")



			elif Evaluar == 'Salida':
				Variable1 = cuadruplo.pop()
				file.write("pinMode(")
				file.write(Variable1)
				file.write(", OUTPUT);")
				file.write("\n")

			elif Evaluar == 'Entrada':
				Variable1 = cuadruplo.pop()
				file.write("pinMode(")
				file.write(Variable1)
				file.write(", INPUT);")
				file.write("\n")

			elif Evaluar == 'Escribir':
				Variable1 = cuadruplo.pop()
				Asignacion = cuadruplo.pop()
				
				if Asignacion == 'high':
					file.write("digitalWrite(")
					file.write(Variable1)
					file.write(", HIGH);")
					file.write("\n")
					
				elif Asignacion == 'low':
					file.write("digitalWrite(")
					file.write(Variable1)
					file.write(", LOW);")
					file.write("\n")

			elif Evaluar == 'LeerDig':
				Variable1 = cuadruplo.pop()
				file.write("digitalRead(")
				file.write(Variable1)
				file.write(");")
				file.write("\n")

			elif Evaluar == 'LeerSerial':
				Variable1 = cuadruplo.pop()
				file.write("Serial.read();")
				file.write("\n")

			elif Evaluar == 'Init_serial':
				Variable1 = cuadruplo.pop()
				if BandCond == True:
					Condicional.append(Evaluar)
					Condicional.append(Variable1)
				else:
					file.write("Serial.begin(9600);")
					file.write("\n")

			elif Evaluar == 'retraso':
				Variable1 = cuadruplo.pop()
				if BandCond == True:
					Condicional.append(Evaluar)
					Condicional.append(Variable1)
				else:
					file.write("delay(")
					file.write(str(Variable1))
					file.write(");")
					file.write("\n")

			elif Evaluar == 'Atras':
				if BandCond == True:
					Condicional.append(Evaluar)

				else:
					file.write("digitalWrite(2, LOW);")
					file.write("\n")
					file.write("digitalWrite(3, HIGH);")
					file.write("\n")

					file.write("digitalWrite(4, LOW);")
					file.write("\n")
					file.write("digitalWrite(5, HIGH);")
					file.write("\n")
					file.write("delay(1000);")
					file.write("\n")

			elif Evaluar == 'print':
				Variable1 = cuadruplo.pop()
				if BandCond == True:
					Condicional.append(Evaluar)
					Condicional.append(Variable1)

				else:
					file.write("Serial.println(")
					file.write(str(Variable1))
					file.write(");")
					file.write("\n")
					

			elif Evaluar == 'setup':
				file.write("void setup(){")
				file.write("\n")
				file.write("Serial.begin(9600);")
				file.write("\n")

			elif Evaluar == 'LOOP:':
				file.write("}")
				file.write("\n")
				file.write("void loop(){")
				file.write("\n")
			

			elif Evaluar == 'goto LOOP':
				file.write("}")
				file.write("\n")

			Evaluar = cuadruplo.pop()


		file.write("}")
		file.write("\n")

		file.close()
