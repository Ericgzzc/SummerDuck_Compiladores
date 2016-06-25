from Scanner import Scanner
import ply.yacc as yacc

class Parser(object):

	palka = ''

	def __init__(self):
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

	def p_error(self,t):
		Parser.error = 1
		if t:
			print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(t.lineno, self.scanner.find_tok_column(t), t.type, t.value))
			#exit(1);
		else:
			print('At end of input')


	def p_programa(self,t):
		"""programa : PROGRAMA ID PUNTOCOMA declara_variables declara_funciones metodo_principal
                    | PROGRAMA ID PUNTOCOMA declara_variables metodo_principal
                    | PROGRAMA ID PUNTOCOMA declara_funciones metodo_principal
                    | PROGRAMA ID PUNTOCOMA metodo_principal
		"""
		if len(t) == 7:
			t[0] = ('programa', t[1], t[2], t[4], t[5],t[6])
			print("Sintaxis correcta")

		elif len(t) == 6:
			t[0] = ('programa', t[1], t[2], t[4], t[5])
			print("Sintaxis correcta")
		else:
			t[0] = ('programa',t[1], t[2], t[4])
			print("Sintaxis correcta")

	def p_declara_variables(self,t):
		"""declara_variables   	: tipo DOSPUNTOS lista_ids PUNTOCOMA
                    			| tipo DOSPUNTOS lista_ids PUNTOCOMA declara_variables
		"""
		if len(t) == 6:
			t[0] = ('declara_variables', t[1], t[3], t[4])
			
		else:
			t[0] = ('declara_variables', t[1], t[3])
			

	def p_tipo(self,t):
		"""tipo 	: ENTERO
                    | REAL
                    | CHAR
		"""
		t[0] = t[1]

	def p_lista_ids(self,t):
		"""lista_ids : variable
                     | variable COMA lista_ids
		"""
		if len(t) == 4:
			t[0] = ('lista_ids', t[1], t[2])
			
		else:
			t[0] = ('lista_ids', t[1])
			

	def p_variable(self,t):
		"""variable : ID
                    | ID indice_matriz
                    | ID indice_matriz indice_matriz
		"""
		if len(t) == 4:
			t[0] = ('variable', t[1], t[2], t[3])
			
		elif len(t) == 3:
			t[0] = ('variable', t[1], t[2])
			
		else:
			t[0] = ('variable', t[1])
			

	def p_indice_matriz(self,t):
		"""indice_matriz : CORIZQ ENTERO CORDER
		"""
		t[0] = ('indice_matriz', t[2])

	def p_declara_funciones(self,t): #7, 6, 8, 7
		"""declara_funciones   	: MODULO tipo_retorno ID PARIZQ lista_parametros PARDER bloque
                    			| MODULO tipo_retorno ID PARIZQ PARDER bloque
                    			| MODULO tipo_retorno ID PARIZQ lista_parametros PARDER bloque declara_funciones
                    			| MODULO tipo_retorno ID PARIZQ PARDER bloque declara_funciones
		"""
		# t[0] = ('declara_funciones', t[1], t[2], t[3], t[4], t[6])
		if len(t) == 9:
			t[0] = ('declara_funciones', t[1], t[2], t[3],t[5],t[7],t[8])
			
		elif len(t) == 8 and t[5] == 'lista_parametros':
			t[0] = ('declara_funciones', t[1], t[2],t[3],t[5],t[7])
			
		elif len(t) == 8 and t[6] == 'bloque':
			t[0] = ('declara_funciones', t[1], t[2],t[3],t[6],t[7])
			
		else:
			t[0] = ('declara_funciones', t[1],t[2],t[3],t[6])
			

	def p_tipo_retorno(self,t):
		"""tipo_retorno : tipo
                     	| VOID
		"""
		t[0] = ('tipo_retorno', t[1])

	def p_lista_parametros(self,t):
		"""lista_parametros : tipo DOSPUNTOS lista_idparam
                    		| tipo DOSPUNTOS lista_idparam lista_parametros
		"""
		if len(t) == 5:
			t[0] = ('lista_parametros', t[1], t[3], t[4])
			
		else:
			t[0] = ('lista_parametros', t[1], t[3])
			

	def p_lista_idparam(self,t):
		"""lista_idparam 	: ID
                    		| ID COMA lista_idparam
		"""
		if len(t) == 4:
			t[0] = ('lista_idparam', t[1], t[3])
			
		else:
			t[0] = ('lista_idparam', t[1])
			

	def p_bloque(self,t): #8 , 7, 7, 6, 7, 6, 6, 5
		"""bloque 	: LLAVEIZQ declara_variables estatutos_control REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ estatutos_control REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ declara_variables REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ REGRESA PARIZQ expresion PARDER LLAVEDER
                    | LLAVEIZQ declara_variables estatutos_control REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ estatutos_control REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ declara_variables REGRESA PARIZQ PARDER LLAVEDER
                    | LLAVEIZQ REGRESA PARIZQ PARDER LLAVEDER 
		"""
		if len(t) == 9:
			t[0] = ('bloque', t[2], t[3], t[4], t[6])
			
		elif len(t) == 7:
			t[0] = ('bloque', t[2],t[3],t[5])
			
		elif len(t) == 6 and t[4] == 'expresion':
			t[0] = ('bloque', t[2],t[4])
			
		elif len(t) == 7 and t[4] == 'REGRESA':
			t[0] = ('bloque', t[2],t[4])
			
		elif len(t) == 6 and t[3] == 'REGRESA':
			t[0] = ('bloque', t[2],t[4])
			
		else:
			t[0] = ('bloque', t[2])
			
		

	def p_metodo_principal(self,t):
		"""metodo_principal    	: PRINCIPAL PARIZQ PARDER LLAVEIZQ declara_variables estatutos_control LLAVEDER
                    			| PRINCIPAL PARIZQ PARDER LLAVEIZQ estatutos_control LLAVEDER
                   				| PRINCIPAL PARIZQ PARDER LLAVEIZQ declara_variables LLAVEDER
                    			| PRINCIPAL PARIZQ PARDER LLAVEIZQ LLAVEDER
		"""
		if len(t) == 8:
			t[0] = ('metodo_principal', t[1], t[5],t[6])
			
		elif len(t) == 7:
			t[0] = ('metodo_principal', t[1],t[5])
			
		else:
			t[0] = ('metodo_principal', t[1])


	def p_estatutos_control(self,t):
		"""estatutos_control   	: estatuto_control PUNTOCOMA
                   				| estatuto_control PUNTOCOMA estatutos_control
		"""
		if len(t) == 4:
			t[0] = ('estatutos_control', t[1], t[3])
			
		else:
			t[0] = ('estatutos_control', t[1])
			

	def p_estatuto(self,t):
		"""estatuto : asignacion
                    | llamada
                    | lectura
                    | escritura
		"""
		t[0] = ('estatuto', t[1])

	def p_estatuto_control(self,t):
		"""estatuto_control    : decision
                    			| repeticion
                    			| estatuto
		"""
		t[0] = ('estatuto_control', t[1])

	def p_asignacion(self,t):
		"""asignacion 	: variable IGUAL expresion
						
		"""
		t[0] = ('asignacion', t[1], t[3])

	def p_llamada(self,t):
		"""llamada 	: ID PARIZQ PARDER
                    | ID PARIZQ lista_valores PARDER
		"""
		if len(t) == 5:
			t[0] = ('llamada', t[1], t[3])
		else:
			t[0] = ('llamada', t[1])

	def p_lectura(self,t):
		"""lectura : LEER PARIZQ lista_valores PARDER
		"""
		t[0] = ('lectura', t[1], t[3])

	def p_escritura(self,t):
		"""escritura : ESCRIBIR PARIZQ lista_valores PARDER
		"""
		t[0] = ('escritura', t[1], t[3])

	def p_decision(self,t):
		"""decision : SI PARIZQ estatuto_control PARDER hacer
                    | SI PARIZQ estatuto_control PARDER SINO hacer
		"""
		if len(t) == 6:
			t[0] = ('decision', t[1], t[3], t[5], t[6])
		else:
			t[0] = ('decision', t[1], t[3], t[5])

	def p_hacer(self,t):
		"""hacer   	: LLAVEIZQ LLAVEDER
                    | LLAVEIZQ estatutos_control LLAVEDER
		"""
		if len(t) == 4:
			t[0] = ('hacer', t[2])
		else:
			t[0] = ('hacer')

	def p_repeticion(self,t):
		"""repeticion 	: mientras
                    	| repite
		"""
		t[0] = ('repeticion', t[1])
	def p_mientras(self,t):
		"""mientras : MIENTRAS PARIZQ estatuto_control PARDER HAZ hacer
		"""
		t[0] = ('mientras', t[1], t[3], t[5],t[6])
	def p_repite(self,t):
		"""repite : REPITE hacer HASTA PARIZQ estatuto_control PARDER 
		"""
		t[0] = ('repite', t[1], t[2], t[3],t[5])

	def p_lista_valores(self,t):
		"""lista_valores 	: estatuto
                    		| estatuto COMA lista_valores
		"""
		if len(t) == 4:
			t[0] = ('lista_valores', t[1],t[3])
		else:
			t[0] = ('lista_valores',t[1])

	def p_expresion(self,t):
		"""expresion 	: expresion AND exp
                    	| expresion OR exp
                    	| expresion NOT exp
                    	| expresion MENORQUE exp
                    	| expresion MAYORQUE exp
                    	| expresion IGUAL exp
                    	| expresion MENORIGUAL exp
                    	| expresion MAYORIGUAL exp
                    	| determinante
                    	| inversa
		"""
		t[0] = ('expresion',t[1])
	def p_expresion2(self, t):
	    'expresion : exp'
	    t[0] = t[1]

	def p_exp(self,t):
		'''exp : exp MAS term
	           | exp MENOS term'''
		t[0] = ('PLUSMINUS', t[2], t[1], t[3])

	def p_exp2(self,t):
		'exp : term'
		t[0] = t[1]

	def p_term(self,t):
		'''term : term MULTI fact
            | term DIV fact'''
		t[0] = ('TIMDIV', t[2], t[1], t[3])

	def p_term2(self,t):
		'term : fact'
		t[0] = t[1]

	def p_fact(self,t):
		'''fact : varcte'''
		t[0] = t[1]
	def p_varcte(self,t):
		'''varcte : ENTERO
              | REAL
              | ID	'''
		t[0] = t[1]

	def p_determinante(self,t):
		"""determinante 	: estatuto PESOS"""
	def p_inversa(self,t):
		"""inversa 		: estatuto INTERROGACION"""

	
