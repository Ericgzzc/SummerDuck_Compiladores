import ply.yacc as yacc
import lex
tokens = lex.tokens


def p_programa(p):
	'''programa :  PROGRAMA ID PUNTOCOMA Variables bloque PRINCIPAL LLAVEIZQ Variables bloque LLAVEDER
	'''
def p_Variables(p):
	'''Variables : Variables1 Variables
			| empty
	'''
def p_Variables1(p): 
	'''Variables1 : Tipo DecVariables DOSPUNTOS
	'''
def p_DecVariables(p):
	'''DecVariables : ID AsigVar RepVars
	'''
def p_RepVars(p):
	'''RepVars : COMA DecVariables
			   | empty
	'''
def p_AsigVar(p):
	'''AsigVar : IGUAL Exp
			   | Exp
	'''
def p_Tipo(p):
	'''Tipo : ENTERO
			| CHAR
			| REAL
			| VOID
			| BOOL
	'''

def p_Bloque(p):
	'''Bloque : Estatuto Bloque
			  | empty
    '''
def p_Estatuto(p):
	'''Estatuto : empty
				| Asigna
				| Cond
				| MIENTRAS
				| LEE
				| ESCRIBE
				| REPITE
	'''		
def p_Asigna(p):
	'''Asigna : ID IGUAL Exp
	'''
def p_Cond(p):
	'''Cond : Cond1
			| empty
	'''
def p_Cond1(p):
	'''Cond1 : SI PARIZQ Cond PARDER LLAVEIZQ Estatuto LLAVEDER ParteElse
	'''
def p_ParteElse(p):
	'''ParteElse : SINO LLAVEIZQ Estatuto LLAVEDER 
				 | empty
	'''
    
def p_vars(p):
	'''vars : Variables vars1
			| empty
	'''
def p_vars1(p):
	'''vars1 : ID id1 DOSPUNTOS tipo PUNTOCOMA vars1
			  | ID id1 DOSPUNTOS tipo PUNTOCOMA 
	'''
def p_id1(p):
	'''id1    : empty 
			  | COMA ID id1
	'''
def p_tipo(p):
	'''tipo : ENTERO
			| REAL
	'''
def p_bloque(p):
	'''bloque : LLAVEIZQ estatuto est1 LLAVEDER
			  | LLAVEIZQ LLAVEDER
	'''
def p_est1(p):
	''' est1 : estatuto est1
			  | empty
	'''
def p_estatuto(p):
	'''estatuto : asignacion
				| condicion
				| escritura
	'''
def p_asignacion(p):
	'''asignacion : ID IGUAL expresion PUNTOCOMA
	'''
def p_escritura(p):
	'''escritura : ESCRIBE PARIZQ expresion esc1 PARDER PUNTOCOMA
				 | ESCRIBE PARIZQ ID esc1 PARDER PUNTOCOMA
	'''
def p_esc1(p):
	'''esc1 : COMA expresion esc1
			 | COMA ID esc1
			 | empty
	'''
def p_expresion(p):
	'''expresion : Exp Exp1
	'''
def p_Exp1(p):
	'''Exp1 : MAYORQUE Exp 
			| MENORQUE Exp
			| DIFERENTE Exp
			| empty
	'''
def p_Exp(p):
	'''Exp : termino Exp2 
    '''
def p_Exp2(p):
	'''Exp2 : MAS termino Exp2
			| MENOS termino Exp2
			| empty
	'''
def p_termino(p) :
 	'''termino : factor term1
 	'''
def p_term1(p):
	'''term1 : MULTI factor term1
			 | DIV factor term1
			 | empty
	'''
def p_condicion(p):
	'''condicion : SI PARIZQ expresion PARDER bloque cond1 PUNTOCOMA
	'''
def p_cond1(p):
	'''cond1 : SINO bloque
			 | empty 
	'''
def p_varcte(p):
	'''varcte : ID
			  | ENTERO	
			  | REAL
	'''
def p_factor(p):
	'''factor : PARIZQ expresion PARDER
			  | fac1 
	'''
def p_fac1(p):
	'''fac1 : varcte
			| MAS varcte
			| MENOS	varcte
	'''
def p_empty(p):
    'empty :'
    pass
def p_error(p):
	print ("Error de sintaxis")
parser = yacc.yacc() 
