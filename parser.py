from Scanner import Scanner
import ply.yacc as yacc

class Parser(object):

	palka = ''

	def __ini_(self):
		self.scanner = Scanner()
		self.scanner.build()

	tokens = Scanner.tokens

	precedence = (
		("nonassoc", 'SI'),
		("nonassoc", 'SINO'),
		("right", 'IGUAL'),
		("left", 'OR'),
		("left", 'AND'),
		("nonassoc", 'MAYORQUE', 'MENORQUE', 'IGUALIGUAL', 'NOT', 'MAYORIGUAL', 'MENORIGUAL'),
		("left", 'MAS', 'MENOS'),
		("left", 'MULTI', 'DIV', 'MOD'),
	)

	error = 0

	def p_error(t):
		Parser.error = 1
		if p:
			print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(t), p.type, p.value))
			#exit(1);
		else:
			print('At end of input')


	def p_programa(t):
		"""programa : PROGRAMA ID PUNTOCOMA declara_variables declara_funciones metodo_principal
                    | PROGRAMA ID PUNTOCOMA declara_variables metodo_principal
                    | PROGRAMA ID PUNTOCOMA declara_funciones metodo_principal
                    | PROGRAMA ID PUNTOCOMA metodo_principal
		"""
		if len(t) == 7:
			t[0] = ('programa', t[4], t[5], t[6])
			print("Sintaxis correcta")

		elif len(t) == 6:
			t[0] = ('programa', t[4], t[5])
			print("Sintaxis correcta")
		else:
			t[0] = ('programa',t[4])
			print("Sintaxis correcta")

	def p_declara_variables(t):
		"""declara_variables   	: tipo DOSPUNTOS lista_ids PUNTOCOMA
                    			| tipo DOSPUNTOS lista_ids PUNTOCOMA declara_variables
		"""
		if len(t) == 7:
			t[0] = ('declara_variables', t[1], t[3], t[4])
			print("Sintaxis correcta")

	def p_tipo(t):
		"""tipo 	: ENTERO
                    | REAL
                    | CHAR
		"""
		t[0] = t[1]

	def p_lista_ids(t):
		"""lista_ids : variable
                     | variable COMA lista_ids
		"""
		if len(t) == 4:
			t[0] = ('lista_ids', t[1], t[2])
			print("Sintaxis correcta")
		else:
			t[0] = ('lista_ids', t[1])

	def p_variable(t):
		"""variable : ID
                    | ID indice_matriz
                    | ID indice_matriz indice_matriz
		"""
		if len(t) == 4:
			t[0] = ('variable', t[1], t[2], t[3])
			print("Sintaxis correcta")
		elif len(t) == 3:
			t[0] = ('variable', t[1], t[2])
			print("Sintaxis correcta")
		else:
			t[0] = ('variable', t[1])
			print("Sintaxis correcta")

	def p_indice_matriz(t):
		"""indice_matriz : CORIZQ ENTERO CORDER
		"""
		t[0] = ('indice_matriz', t[2])

	def p_declara_funciones(t):
		"""declara_funciones   	: MODULO tipo_retorno ID PARIZQ lista_parametros PARDER bloque
                    			| MODULO tipo_retorno ID PARIZQ PARDER bloque
                    			| MODULO tipo_retorno ID PARIZQ lista_parametros PARDER bloque declara_funciones
                    			| MODULO tipo_retorno ID PARIZQ PARDER bloque declara_funciones
		"""
		t[0] = ('declara_funciones', t[1], t[2], t[3], t[4], t[6])

	def p_tipo_retorno(t):
		"""tipo_retorno : tipo
                     	| VOID
		"""
		t[0] = ('tipo_retorno', t[1])

	def p_lista_parametros(t):
		"""lista_parametros : tipo DOSPUNTOS lista_idparam
                    		| tipo DOSPUNTOS lista_idparam lista_parametros
		"""
		t[0] = ('lista_parametros', t[1], t[3], t[4])

	def p_lista_idparam(t):
		"""lista_idparam 	: ID
                    		| ID COMA lista_idparam
		"""
		if len(t) == 4:
			t[0] = ('lista_idparam', t[1], t[3])
			print("Sintaxis correcta")
		else:
			t[0] = ('lista_idparam', t[1])
			print("Sintaxis correcta")

	def p_bloque(t):
		"""bloque 	: LLAVEIZQ declara_variables estatutos_control REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ estatutos_control REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ declara_variables REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ declara_variables estatutos_control REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ estatutos_control REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ declara_variables REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ REGRESA PARIZQ PARDER LLAVEDER 
		"""
		t[0] = ('bloque', t[2], t[3], t[4], t[5])

	def p_metodo_principal(t):
		"""metodo_principal    	: PRINCIPAL PARIZQ PARDER LLAVEIZQ declara_variables estatutos_control LLAVEDER
                    			| PRINCIPAL PARIZQ PARDER LLAVEIZQ estatutos_control LLAVEDER
                   				| PRINCIPAL PARIZQ PARDER LLAVEIZQ declara_variables LLAVEDER
                    			| PRINCIPAL PARIZQ PARDER LLAVEIZQ LLAVEDER
		"""
		t[0] = ('metodo_principal', t[1], t[5], t[6])

	def p_estatutos(t):
		"""estatutos 	: estatuto PUNTOCOMA
                    	| estatuto PUNTOCOMA estatutos
		"""
		if len(t) == 4:
			t[0] = ('estatutos', t[1], t[3])
		else:
			t[0] = ('estatutos', t[1])

	def p_estatutos_control(t):
		"""estatutos_control   	: estatuto_control PUNTOCOMA
                   				| estatuto_control PUNTOCOMA estatutos_control
		"""

	def p_estatuto(t):
		"""estatuto : asignacion
                    | llamada
                    | lectura
                    | escritura
                    | expresion
		"""
		t[0] = ('estatuto', t[1])

	def p_estatuto_control(t):
		"""estatuto_control    : decision
                    			| repeticion
                    			| estatuto
		"""

	def p_asignacion(t):
		"""asignacion : variable IGUAL estatuto_control
		"""
		t[0] = ('asignacion', t[1], t[3])

	def p_llamada(t):
		"""llamada 	: ID PARIZQ PARDER
                    | ID PARIZQ lista_valores PARDER
		"""
		t[0] = ('llamada', t[1], t[3])

	def p_lectura(t):
		"""lectura : LEER PARIZQ lista_valores PARDER
		"""
		t[0] = ('lectura', t[1], t[3])

	def p_escritura(t):
		"""escritura : ESCRIBIR PARIZQ lista_valores PARDER
		"""
		t[0] = ('escritura', t[1], t[3])

	def p_decision(t):
		"""decision : SI PARIZQ estatuto_control PARDER hacer
                    | SI PARIZQ estatuto_control PARDER SINO LLAVEIZQ estatutos_control LLAVEDER hacer
		"""
		if len(t) == 9:
			t[0] = ('decision', t[1], t[3], t[5], t[6])
		else:
			t[0] = ('decision', t[1], t[3])

	def p_hacer(t):
		"""hacer   	: LLAVEIZQ LLAVEDER
                    | LLAVEIZQ estatutos_control LLAVEDER
		"""

	def p_repeticion(t):
		"""repeticion : mientras
                    | repite
		"""
		t[0] = ('repeticion', t[1])
	def p_mientras(t):
		"""mientras : MIENTRAS PARIZQ estatuto_control PARDER HAZ hacer
		"""
		t[0] = ('mientras', t[1], t[3], t[5],t[7])
	def p_repite(t):
		"""repite : REPITE hacer HASTA PARIZQ estatuto_control PARDER 
		"""
		t[0] = ('repite', t[1], t[3], t[5],t[7])

	def p_lista_valores(t):
		"""lista_valores 	: estatuto
                    		| estatuto COMA lista_valores
		"""

	def p_expresion(t):
		"""expresion 	: suma
                    	| resta
                    	| multiplicacion
                    	| division
                    	| biand
                    	| bior
                    	| binot
                    	| menor_que
                    	| mayor_que
                    	| equals
                    	| menor_igual
                    	| mayor_igual
                    	| determinante
                    	| inversa
		"""
	def p_suma(t):
		"""suma : estatuto MAS estatuto"""
	def p_resta(t):
		"""resta	: estatuto MENOS estatuto"""
	def p_multiplicacion(t):
		"""multiplicacion	: estatuto MULTI estatuto"""
	def p_division(t):
		"""division	: estatuto DIV estatuto"""
	def p_biand(t):
		"""biand	: estatuto AND estatuto"""
	def p_bior(t):
		"""bior	: estatuto OR estatuto"""
	def p_binot(t):
		"""binot	: estatuto NOT estatuto"""
	def p_menor_que(t):
		"""menor_que	: estatuto MENORQUE estatuto"""
	def p_mayor_que(t):
		"""mayor_que	: estatuto MAYORQUE estatuto"""
	def p_equals(t):
		"""equals	: estatuto IGUALIGUAL estatuto"""
	def p_menor_igual(t):
		"""menor_igual	: estatuto MENORIGUAL estatuto"""
	def p_mayor_igual(t):
		"""mayor_igual 	: estatuto MAYORIGUAL estatuto"""
	def p_determinante(t):
		"""determinante 	: estatuto PESOS"""
	def p_inversa(t):
		"""inversa 		: estatuto INTERROGACION"""

	
