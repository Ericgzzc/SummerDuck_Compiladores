#
#Proyecto
#Lexico
#
#

import sys
sys.path.insert(0,"../..")
import ply.lex as lex


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


# Completely ignored characters
t_ignore           = ' \t\x0c'

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Operators
t_MAS           	= r'\+'
t_MENOS         	= r'-'
t_MULTI         	= r'\*'
t_DIV           	= r'/'
t_MOD              	= r'%'
t_ANDBIT           	= r'&'
t_OR              	= r'\|\|'
t_AND            	= r'&&'
t_NOT             	= r'!'
t_MAYORQUE         	= r'<'
t_MENORQUE         	= r'>'
t_MAYORIGUAL      	= r'<='
t_MENORIGUAL      	= r'>='
t_IGUALIGUAL       	= r'=='
t_DIFERENTE        	= r'!='


# Assignment operators

t_IGUAL           	= r'='
t_IGUALPOR       	= r'\*='
t_IGUALDIV         	= r'/='
t_IGUALMOD         	= r'%='
t_IGUALMAS       	= r'\+='
t_IGUALMENOS        = r'-='

# Increment/decrement
t_MASMAS          = r'\+\+'
t_MENOSMENOS      = r'--'

# ?
t_CONDOP           = r'\?'


# Delimeters
t_PARIZQ          	= r'\('
t_PARDER          	= r'\)'
t_CORDER         	= r'\]'
t_CORIZQ         	= r'\['
t_LLAVEDER         	= r'\}'
t_LLAVEIZQ        	= r'\{'
t_COMA           	= r','
t_PUNTO          	= r'\.'
t_PUNTOCOMA       	= r';'
t_DOSPUNTOS        	= r':'
t_COMILLAS        	= r'"'
t_GATO				= r'\#'
t_ELLIPSIS         	= r'\.\.\.'



# Identifiers and reserved words

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = str(t.value)
    t.type = reserved_map.get(t.value,"ID")
    return t

def t_CHAR(t):
    r'"(\\.|[^\\"])*\"'
    t.value = str(t.value)
    t.type = reserved_map.get(t.value,"CHAR")
    return t

def t_REAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    t.type = reserved_map.get(t.value,"REAL")
    return t

def t_ENTERO(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = reserved_map.get(t.value,"ENTERO")
    return t
	

def t_comment(t):
    r' %%(.|\n)*?%%'
    t.lineno += t.value.count('\n')


def t_error(t):
    print("CARACTER NO DEFINIDO: '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(optimize=1,lextab="tab")


if __name__ == '__main__':
    lex.runmain()