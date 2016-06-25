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
		"""programa : PROGRAMA t_ID t_PUNTOCOMA declara_variables declara_funciones metodo_principal
                    | PROGRAMA t_ID t_PUNTOCOMA declara_variables metodo_principal
                    | PROGRAMA t_ID t_PUNTOCOMA declara_funciones metodo_principal
                    | PROGRAMA t_ID t_PUNTOCOMA metodo_principal
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
		"""declara_variables   	: tipo t_DOSPUNTOS lista_ids t_PUNTOCOMA
                    			| tipo t_DOSPUNTOS lista_ids t_PUNTOCOMA declara_variables
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
                     | variable t_COMA lista_ids
		"""
		if len(t) == 4:
			t[0] = ('lista_ids', t[1], t[2])
			print("Sintaxis correcta")
		else
			t[0] = ('lista_ids', t[1])

	def p_variable(t):
		"""variable : t_ID
                    | t_ID indice_matriz
                    | t_ID indice_matriz indice_matriz
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
		"""indice_matriz : t_CORIZQ t_ENTERO t_CORDER
		"""
		t[0] = ('indice_matriz', t[2])

	def p_declara_funciones(t):
		"""declara_funciones   	: MODULO tipo_retorno t_ID t_PARIZQ lista_parametros t_PARDER bloque
                    			| MODULO tipo_retorno t_ID t_PARIZQ t_PARDER bloque
                    			| MODULO tipo_retorno t_ID t_PARIZQ lista_parametros t_PARDER bloque declara_funciones
                    			| MODULO tipo_retorno t_ID t_PARIZQ t_PARDER bloque declara_funciones
		"""
		t[0] = ('declara_funciones', t[1], t[2], t[3], t[4], t[6])

	def p_tipo_retorno(t):
		"""tipo_retorno : tipo
                     	| VOID
		"""
		t[0] = ('tipo_retorno', t[1])

	def p_lista_parametros(t):
		"""lista_parametros : tipo t_DOSPUNTOS lista_idparam
                    		| tipo t_DOSPUNTOS lista_idparam lista_parametros
		"""
		t[0] = ('lista_parametros', t[1], t[3], t[4])

	def p_lista_idparam(t):
		"""lista_idparam 	: t_ID
                    		| t_ID t_COMA lista_idparam
		"""
		if len(t) == 4:
			t[0] = ('lista_idparam', t[1], t[3])
			print("Sintaxis correcta")
		else
			t[0] = ('lista_idparam', t[1])
			print("Sintaxis correcta")

	def p_bloque(t):
		"""bloque 	: t_LLAVEIZQ declara_variables estatutos_control REGRESA t_PARIZQ expresion t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ estatutos_control REGRESA t_PARIZQ expresion t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ declara_variables REGRESA t_PARIZQ expresion t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ REGRESA t_PARIZQ expresion t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ declara_variables estatutos_control REGRESA t_PARIZQ t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ estatutos_control REGRESA t_PARIZQ t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ declara_variables REGRESA t_PARIZQ t_PARDER t_LLAVEDER
                    | t_LLAVEIZQ REGRESA t_PARIZQ t_PARDER t_LLAVEDER 
		"""
		t[0] = ('bloque', t[2], t[3], t[4], t[5])

	def p_metodo_principal(t):
		"""metodo_principal    	: PRINCIPAL t_PARIZQ t_PARDER t_LLAVEIZQ declara_variables estatutos_control t_LLAVEDER
                    			| PRINCIPAL t_PARIZQ t_PARDER t_LLAVEIZQ estatutos_control t_LLAVEDER
                   				| PRINCIPAL t_PARIZQ t_PARDER t_LLAVEIZQ declara_variables t_LLAVEDER
                    			| PRINCIPAL t_PARIZQ t_PARDER t_LLAVEIZQ t_LLAVEDER
		"""
		t[0] = ('metodo_principal', t[1], t[5], t[6])

	def p_estatutos(t):
		"""estatutos 	: estatuto t_PUNTOCOMA
                    	| estatuto t_PUNTOCOMA estatutos
		"""
		if len(t) == 4:
			t[0] = ('estatutos', t[1], t[3])
		else
			t[0] = ('estatutos', t[1])

	def p_estatutos_control(t):
		"""estatutos_control   	: estatuto_control t_PUNTOCOMA
                   				| estatuto_control t_PUNTOCOMA estatutos_control
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
		"""llamada 	: t_ID t_PARIZQ t_PARDER
                    | t_ID t_PARIZQ lista_valores t_PARDER
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
		"""decision : SI t_PARIZQ estatuto_control t_PARDER hacer
                    | SI t_PARIZQ estatuto_control t_PARDER SINO t_LLAVEIZQ estatutos_control t_LLAVEDER hacer
		"""
		if len(t) == 9:
			t[0] = ('decision', t[1], t[3], t[5], t[6])
		else
			t[0] = ('decision', t[1], t[3])

	def p_hacer(t):
		"""hacer   	: t_LLAVEIZQ t_LLAVEDER
                    | t_LLAVEIZQ estatutos_control t_LLAVEDER
		"""

	def p_repeticion(t):
		"""repeticion : mientras
                    | repite
		"""
		t[0] = ('repeticion', t[1])
	def p_mientras(t):
		"""mientras : MIENTRAS t_PARIZQ estatuto_control t_PARDER HAZ hacer
		"""
		t[0] = ('mientras', t[1], t[3], t[5],t[7])
	def p_repite(t):
		"""repite : REPITE hacer HASTA t_PARIZQ estatuto_control t_PARDER 
		"""
		t[0] = ('repite', t[1], t[3], t[5],t[7])

	def p_lista_valores(t):
		"""lista_valores 	: estatuto
                    		| estatuto t_COMA lista_valores
		"""

	def p_expresion(t):
		"""expresion : suma
                    | resta
                    | multiplicacion
                    | division
                    | bit_and
                    | bit_or
                    | bit_not
                    | menor_que
                    | mayor_que
                    | equals
                    | menor_igual
                    | mayor_igual
                    | determinante
                    | inversa
		"""
		def p_suma(t):
			"""suma 	: estatuto t_MAS estatuto"""
		def p_resta(t):
			"""resta	: estatuto t_MENOS estatuto"""
		def p_multiplicacion(t):
			"""multiplicacion	: estatuto t_MULI estatuto"""
		def p_division(t):
			"""division	: estatuto t_DIV estatuto"""
		def p_bit_and(t):
			"""bit_and	: estatuto t_AND estatuto"""
		def p_bit_or(t):
			"""bit_or	: estatuto t_OR estatuto"""
		def p_bit_not(t):
			"""bit_not	: estatuto t_NOT estatuto"""
		def p_menor_que(t):
			"""menor_que	: estatuto t_MENORQUE estatuto"""
		def p_mayor_que(t):
			"""mayor_que	: estatuto t_MAYORQUE estatuto"""
		def p_equals(t):
			"""equals	: estatuto t_IGUALIGUAL estatuto"""
		def p_menor_igual(t):
			"""menor_igual	: estatuto t_MENORIGUAL estatuto"""
		def p_mayor_igual(t):
			"""mayor_igual 	: estatuto t_MAYORIGUAL estatuto"""
		def p_determinante(t):
			"""determinante 	: estatuto t_PESOS"""
		def p_inversa(t):
			"""inversa 		: estatuto t_INTERROGACION"""

	
