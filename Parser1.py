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
		"""programa : PROGRAMA ID PUNTOCOMA estatutos_dec_vars declara_funciones metodo_principal
					| PROGRAMA ID PUNTOCOMA declara_funciones metodo_principal
					| PROGRAMA ID PUNTOCOMA metodo_principal
		"""
		if len(t) == 7:
			t[0] = AST.Programa( t[4], t[5], t[6])
			print("Sintaxis correcta")

		elif len(t) == 6:
			t[0] = AST.Programa('None', t[4], t[5])
			print("Sintaxis correcta")
		else:
			t[0] = AST.Programa('None','None',t[4])
			print("Sintaxis correcta")

	def p_declara_variables(t):
		"""declara_variables	: tipo DOSPUNTOS lista_ids declara_variables
                    			| empty
		"""
		if len(t) == 7:
			t[0] = AST.Declara_variables(t[1], t[3], t[4])
			print("Sintaxis correcta")
		else
			t[0] = AST.Empty()

	def p_estatutos_dec_vars(t):
		"""estatutos_dec_vars 	: tipo DOSPUNTOS lista_ids PUNTOCOMA estatutos_dec_vars
        						| empty
		"""
		if len(t) == 7:
			t[0] = AST.Estatutos_dec_vars( t[1], t[3], t[4])
			print("Sintaxis correcta")
		else
			t[0] = AST.Empty()

	def p_tipo(t):
		"""tipo : ENTERO
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
		else
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
		else
			t[0] = ('variable', t[1])
			print("Sintaxis correcta")

	def p_indice_matriz(t):
		"""indice_matriz 	: CORDER ENTERO COR
		"""
		t[0] = ('indice_matriz', t[2])

	def p_declara_funciones(t):
		"""declara_funciones   	: MODULO tipo_retorno ID PARIZQ lista_parametros PARDER bloque declara_funciones
                    			| empty
		"""
		t[0] = ('declara_funciones', t[1], t[2], t[3], t[4], t[6])

	def p_tipo_retorno(t):
		"""tipo_retorno : tipo
                     	| VOID
		"""
		t[0] = ('tipo_retorno', t[1])

	def p_lista_parametros(t):
		"""lista_parametros : tipo DOSPUNTOS lista_idparam lista_parametros
                    		| empty
		"""
		t[0] = ('lista_parametros', t[1], t[3], t[4])

	def p_lista_idparam(t):
		"""lista_idparam 	: ID
                    		| ID COMA lista_idparam
		"""
		if len(t) == 4:
			t[0] = ('lista_idparam', t[1], t[3])
			print("Sintaxis correcta")
		else
			t[0] = ('lista_idparam', t[1])
			print("Sintaxis correcta")

	def p_bloque(t):
		"""bloque : LLAVEIZQ declara_variables estatutos REGRESA PARIZQ expresion PARDER LLAVEDER
		"""
		t[0] = ('bloque', t[2], t[3], t[4], t[5])

	def p_metodo_principal(t):
		"""metodo_principal 	: PRINCIPAL PARIZQ PARDER LLAVEIZQ declara_variables estatutos LLAVEDER
		"""
		t[0] = ('metodo_principal', t[1], t[5], t[6])

	def p_estatutos(t):
		"""estatutos : estatuto
                    | estatuto PUNTOCOMA estatutos
                    | empty
		"""
		if len(t) == 4:
			t[0] = ('estatutos', t[1], t[3])
		else
			t[0] = ('estatutos', t[1])

	def p_estatuto(t):
		"""estatuto : asignacion
                    | llamada
                    | lectura
                    | escritura
                    | decision
                    | repeticion
                    | expresion
		"""
		t[0] = ('estatuto', t[1])

	def p_asignacion(t):
		"""asignacion : variable IGUAL estatuto
		"""
		t[0] = ('asignacion', t[1], t[3])

	def p_llamada(t):
		"""llamada : ID PARIZQ lista_valores PARDER
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
		"""decision : SI PARIZQ estatuto PARDER
                    | SI PARIZQ estatuto PARDER SINO LLAVEIZQ estatutos LLAVEDER
		"""
		if len(t) == 9:
			t[0] = ('decision', t[1], t[3], t[5], t[6])
		else
			t[0] = ('decision', t[1], t[3])

	def p_repeticion(t):
		"""repeticion : mientras
                    | repite
		"""
		t[0] = ('repeticion', t[1])
	def p_mientras(t):
		"""mientras : MIENTRAS PARIZQ estatuto PARDER HAZ LLAVEIZQ estatutos LLAVEDER
		"""
		t[0] = ('mientras', t[1], t[3], t[5],t[7])
	def p_repite(t):
		"""repite : REPITE LLAVEIZQ estatutos LLAVEDER HASTA PARIZQ estatuto PARDER
		"""
		t[0] = ('repite', t[1], t[3], t[5],t[7])
