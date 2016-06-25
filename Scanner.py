import ply.lex as lex

class Scanner(object):
    def find_tok_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        return token.lexpos - last_cr


    def build(self):
        self.lexer = lex.lex(object=self)

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
      'lee':'LEER',
      'escribe':'ESCRIBIR',
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
		"ID",

		# Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=), %%
		"MAS", "MENOS", "MULTI", "DIV", "MOD",
		"OR", "AND", "NOT", "ANDBIT",
		"MAYORQUE","MENORQUE","MAYORIGUAL", "MENORIGUAL" , "IGUALIGUAL" ,"DIFERENTE", "DOBLEPORCENTAJE",

		# Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
		"IGUAL",

		# Increment/decrement (++,--)
		"MASMAS", "MENOSMENOS",

		# Conditional operator (?)
		"INTERROGACION",

		# Delimeters ( ) [ ] { } , . ; :
		"PARIZQ", "PARDER",
		"CORDER", "CORIZQ",
		"LLAVEIZQ", "LLAVEDER",
		"COMA", "PUNTO", "PUNTOCOMA", "DOSPUNTOS", "COMILLAS", "PESOS",
    ] + list(reserved.values())


    t_ignore = ' \t\f'

    error = 0

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    t_MAS = r'\+'
    t_MENOS = r'-'
    t_MULTI = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'
    t_ANDBIT = r'&'
    t_OR = r'\|\|'
    t_AND = r'&&'
    t_NOT = r'!'
    t_MAYORQUE = r'<'
    t_MENORQUE = r'>'
    t_MAYORIGUAL = r'<='
    t_MENORIGUAL = r'>='
    t_IGUALIGUAL = r'=='
    t_DIFERENTE = r'!='


	# Assignment operators

    t_IGUAL = r'='


	# Increment/decrement
    t_MASMAS = r'\+\+'
    t_MENOSMENOS = r'--'

	# ?
    t_INTERROGACION = r'\?'

	# Delimeters
    t_PARIZQ = r'\('
    t_PARDER = r'\)'
    t_CORDER = r'\]'
    t_CORIZQ = r'\['
    t_LLAVEDER = r'\}'
    t_LLAVEIZQ = r'\{'
    t_COMA = r','
    t_PUNTO = r'\.'
    t_PUNTOCOMA = r';'
    t_DOSPUNTOS = r':'
    t_COMILLAS = r'"'
    t_PESOS = r'\$'

    def t_comment(self, t):
        r' %%(.|\n)*?%%'
        t.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        Scanner.error = 1;
        t.lexer.skip(1)


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = str(t.value)
        t.type = "ID"
        return t

    def t_CHAR(self, t):
        r'"(\\.|[^\\"])*\"'
        t.value = str(t.value)
        t.type = "CHAR"
        return t

    def t_REAL(self, t):
        r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        t.type = "REAL"
        return t

    def t_ENTERO(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        t.type = "ENTERO"
        return t
