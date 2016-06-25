import ply.lex as lex

class Scanner(object):

	def build(self):
		self.lexer = lex.lex(object=self)

	def find_tok_column(self, token):
		last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
		if last_cr < 0:
			last_cr = 0
		return token.lexpos - last_cr

	def input(self, text):
		self.lexer.input(text)

	def token(self):
		return self.lexer.token()

	reserved = {
		'programa':'PROGRAMA',
		'principal':'PRINCIPAL',
		'entero':'ENTERO',
		'real':'REAL',
		'char':'CHAR',
		'modulo':'MODULO',
		'regresa':'REGRESA',
		'lee':'LEE',
		'escribe':'ESCRIBE',
		'si':'SI',
		'entonces':'ENTONCES',
		'sino':'SINO',
		'mientras':'MIENTRAS',
		'haz':'HAZ' ,
		'repite':'REPITE',
		'hasta':'HASTA' ,
		'void':'VOID',
		'bool':'BOOL',
	}

	tokens = [
		# Literals (identifier, integer constant, float constant, string constant, char const)
		"ID", "TYPEID", "ICONST", "FCONST", "SCONST", "CCONST",

		# Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=), %%
		"MAS", "MENOS", "MULTI", "DIV", "MOD",
		"OR", "AND", "NOT", "ANDBIT",
		"MAYORQUE","MENORQUE","MAYORIGUAL", "MENORIGUAL" , "IGUALIGUAL" ,"DIFERENTE", "DOBLEPORCENTAJE",

		# Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
		"IGUAL", "IGUALPOR", "IGUALDIV", "IGUALMOD", "IGUALMAS", "IGUALMENOS",

		# Increment/decrement (++,--)
		"MASMAS", "MENOSMENOS",

		# Conditional operator (?)
		"INTERROGACION",

		# Delimeters ( ) [ ] { } , . ; :
		"PARIZQ", "PARDER",
		"CORDER", "CORIZQ",
		"LLAVEIZQ", "LLAVEDER",
		"COMA", "PUNTO", "PUNTOCOMA", "DOSPUNTOS", "COMILLAS", "PESOS"
	] + list(reserved.values())


    # Completely ignored characters
	t_ignore = ' \t\x0c'

    # Newlines
	def t_NEWLINE(self, t):
		r'\n+'
		t.lexer.lineno += t.value.count("\n")

	t_MAS 				= r'\+'
	t_MENOS 			= r'-'
	t_MULTI				= r'\*'
	t_DIV 				= r'/'
	t_MOD 				= r'%'
	t_ANDBIT 			= r'&'
	t_OR 				= r'\|\|'
	t_AND 				= r'&&'
	t_NOT 				= r'!'
	t_MAYORQUE 			= r'<'
	t_MENORQUE 			= r'>'
	t_MAYORIGUAL 		= r'<='
	t_MENORIGUAL 		= r'>='
	t_IGUALIGUAL 		= r'=='
	t_DIFERENTE 		= r'!='


	# Assignment operators

	t_IGUAL 			= r'='
	t_IGUALPOR  		= r'\*='
	t_IGUALDIV			= r'/='
	t_IGUALMOD 			= r'%='
	t_IGUALMAS 			= r'\+='
	t_IGUALMENOS		= r'-='

	# Increment/decrement
	t_MASMAS 			= r'\+\+'
	t_MENOSMENOS 		= r'--'

	# ?
	t_INTERROGACION 	= r'\?'

	# Delimeters
	t_PARIZQ			= r'\('
	t_PARDER			= r'\)'
	t_CORDER			= r'\]'
	t_CORIZQ			= r'\['
	t_LLAVEDER			= r'\}'
	t_LLAVEIZQ			= r'\{'
	t_COMA 				= r','
	t_PUNTO 			= r'\.'
	t_PUNTOCOMA 		= r';'
	t_DOSPUNTOS 		= r':'
	t_COMILLAS 			= r'"'
	t_PESOS				= r'\$'

	def t_comment(self, t):
		r' %%(.|\n)*?%%'
		t.lineno += t.value.count('\n')

	def t_error(self, t):
		print("CARACTER NO DEFINIDO: '%s'" % t.value[0])
		t.lexer.skip(1)


	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z0-9_]*'
		t.value = str(t.value)
		t.type = reserved.get(t.value,"ID")
		return t

	def t_CHAR(self, t):
		r'"(\\.|[^\\"])*\"'
		t.value = str(t.value)
		t.type = reserved.get(t.value,"CHAR")
		return t

	def t_REAL(self, t):
		r'[0-9]+\.[0-9]+'
		t.value = float(t.value)
		t.type = reserved.get(t.value,"REAL")
		return t

	def t_ENTERO(self, t):
		r'[0-9]+'
		t.value = int(t.value)
		t.type = reserved.get(t.value,"ENTERO")
		return t
