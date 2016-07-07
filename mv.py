from __future__ import print_function
from collections import deque
from Symboltable import *
from io import StringIO
import sys
import tokenize
import re

class Scope:

    def __init__(self,):
        self.variables_scope = {}
        self.name = ""
        self.param = 0
        self.num_param = 0

def get_input(*args, **kw):
    """Read a string from standard input."""
    if sys.version[0] == "2":
        return raw_input(*args, **kw)
    else:
        return input(*args, **kw)


class Stack(deque):
	push = deque.append
	
	def top(self):
		return self[-1]

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

class Machine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.return_stack = Stack()
        self.modulo_stack = Stack()
        self.scope_stack = Stack()
        self.llamada_prep = Stack()
        self.instruction_pointer = 0
        self.code = code
        self.param = 0
        self.table = SymbolTable(None, 'global')
        self.operations = {
            "%":       		self.mod,
            "*":        	self.mul,
            "+":        	self.plus,
            "-":        	self.minus,
            "/":        	self.div,
            "==":       	self.condicion,
            "=":       		self.asigna,
            "<":       		self.condicion,
            ">":       		self.condicion,
            "&&":       	self.condicion,
            "||":       	self.condicion,
            "<=":       	self.condicion,
            ">=":       	self.condicion,
        }
        self.modulos = {
        	"programa": 	self.programa,
        	"principal": 	self.principal,
        	"modulo": 		self.modulo,
        }
        self.variables = {
         	"param": 		self.parametro,
 		  	"global": 		self.global1,
            "local": 		self.local,
           
 		}

        self.dis_map = {
            "regresa": 		self.regresa,
            "principal": 	self.principal,
            "gotof":       	self.si,
            "end_si":       self.end_si,
            "repite":       self.repite,
            "hasta":       	self.hasta,
            "mientras":     self.mientras,
            "end_mientras":	self.end_mientras,
            "llamada":		self.llamada,
            "escribe":		self.print,
            "leer":     	self.read,
            "jmp":      	self.jmp,
            "goto":      	self.goto,
            "gosub":      	self.gosub,
            "over":     	self.over,
            "println":  	self.println,
            "stack":    	self.dump_stack,
            "exit":     	self.exit,
        }
    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()

    def run(self):
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode, self.table)

    def dispatch(self, quadruplo, table):
        # print(quadruplo)
        # quad1 = quadruplo.split(",")
        # quad = []
        # for item in quad1:
        # 	term = re.sub(r'["|\[|\]|]', '', item)
        # 	quad = quad + [term,]
        # op = quad[0]
        # print(quad)
        # print(self.instruction_pointer)
        op = quadruplo[0]
        print("dispatch", self.instruction_pointer, quadruplo)
        if op in self.operations:
            self.operations[op](quadruplo, table)
        elif op in self.modulos:
        	self.modulos[op](quadruplo, table)
        elif op in self.variables:
        	self.variables[op](quadruplo, table)
       	elif op in self.dis_map:
            self.dis_map[op](quadruplo, table)
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    def programa(self, quadruplo, table):
        scope = Scope()
        scope.name ="global"
        self.scope_stack.push(scope)

    def global1(self, quadruplo, table):
        varglobal, tipo, var = quadruplo
        self.scope_stack.top().variables_scope[var]=None
        table.put(VariableSymbol(var, tipo))
    	
    def modulo(self,quadruplo, table): 

        # print(quadruplo)
        self.scope_stack.top().param = self.scope_stack.top().num_param
        # print(self.scope_stack.top().num_param)	
        mod, tipo, nombre = quadruplo
        # funcSymbol = FunctionSymbol(nombre, tipo, [], [], self.instruction_pointer)
        # print(funcSymbol.pointer)
        # self.modulo_stack.push(funcSymbol)
        
    def parametro(self,quadruplo, table): 
        if self.llamada_prep:
        	parame, var = quadruplo
        	self.llamada_prep.top().variables_scope["param"+str(self.llamada_prep.top().param)] = self.buscaVariable(var)
        	self.llamada_prep.top().param = self.llamada_prep.top().param-1
        else:
        	parame,tipo, var = quadruplo
        	var1 = self.scope_stack.top().variables_scope["param"+str(self.scope_stack.top().param)]
        	self.scope_stack.top().variables_scope[var]=var1
        	self.scope_stack.top().param = self.scope_stack.top().param-1
        	

    def local(self, quadruplo, table): 
            local, tipolocal, varlocal = quadruplo
            self.scope_stack.top().variables_scope[varlocal]=None
            table.put(VariableSymbol(varlocal, tipolocal))
    
    def regresa(self, quadruplo, table): 
        print("regresa quad", self.instruction_pointer, quadruplo)
        # print("regresa vars_stock",self.instruction_pointer, self.scope_stack.top().variables_scope)

        if len(quadruplo) == 2:
        	regresa, var = quadruplo
        else:
        	regresa = quadruplo

       
        varx = self.buscaVariable(var)

        # print("regresa var", self.instruction_pointer,var)
        # print("regresa varx", self.instruction_pointer,varx)
        print("regresa varx", self.instruction_pointer,varx)
        variable_regresa =  self.return_stack.top()["return_variable"]
        self.return_stack.top()[variable_regresa]=varx
        self.instruction_pointer =  self.return_stack.top()["pointer"]


        # print("regresa pointer", self.return_stack.top()["pointer"])
        # print("regresa vars_stock",self.instruction_pointer, self.scope_stack.top().variables_scope)
        # print("regresa vars_return", self.return_stack.top())

        self.return_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.top().variables_scope[variable_regresa]=varx

    def goto(self, quadruplo, table):
       	got, line = quadruplo
        if isinstance(line, int) and 0 <= line < len(self.code):
            self.instruction_pointer = line
        else:
            raise RuntimeError("GOTO address must be a valid integer.")

    def gosub(self, quadruplo, table):
        goto, var, line = quadruplo
        returnS = {}
        returnS[var]=None
        returnS["return_variable"]=var
        returnS["pointer"]=self.instruction_pointer
        if isinstance(line, int) and 0 <= line < len(self.code):
            self.instruction_pointer = line
            self.return_stack.push(returnS)
            if self.llamada_prep:
            	self.scope_stack.push(self.llamada_prep.top())
            	self.llamada_prep.pop()
            print("goto",self.scope_stack.top().name)
        else:
            raise RuntimeError("GOTO address must be a valid integer.")

    def principal(self,quadruplo, table): 
    	
    	principal = Scope()
    	principal.name = "principal"
    	self.scope_stack.push(principal)
        
    def si(self, quadruplo, table): 
        # print(quadruplo)
        # print("si",self.scope_stack.top().variables_scope)
        si, var, num = quadruplo
        # print(num)
        varx = self.buscaVariable(var)
        # print(" - type %s, value '%s'" % (type(varx), varx))
        if not varx:
        	self.instruction_pointer=num



    def end_si(self): 
        pass
    def repite(self): 
        pass
    def hasta(self): 
        pass
    def mientras(self): 
        pass
    def end_mientras(self): 
        pass
    def llamada(self, quadruplo, table): 
        tipo, name, num = quadruplo
        scope_llamada = Scope()
        scope_llamada.name = name
        scope_llamada.param = num
        scope_llamada.num_param = num
        self.llamada_prep.push(scope_llamada)
        # param = self.code[self.instruction_pointer:self.instruction_pointer+num]
        # for item in param:
        #     var = self.buscaVariable(item[1])
        #     scope_llamada.variables_scope[item[1]]=var
        # print("llamada", self.instruction_pointer+num+1)
        # self.instruction_pointer = self.instruction_pointer+num
        

    def print(self): 
        pass
    def read(self): 
        pass
    def asigna(self, quadruplo, table):
        # print("asigna", quadruplo)

        igual, res, vac, var = quadruplo
        result = self.buscaVariable(res)
        try:
	        self.scope_stack.top().variables_scope[var]=result
        except:
	        self.scope_stack[0].variables_scope[var]=result

    def buscaVariable(self,var):
    	try:
    		x = self.scope_stack.top().variables_scope[var]
    		return x
    	except:
    		try:
    			x = self.scope_stack[0].variables_scope[var]
    			return x
    		except:
    			return var

    def getValores(self, var1, var2, table):
    	if not table.get(var1) and not table.get(var2):
    		return self.buscaVariable(var1), self.buscaVariable(var2)
    	elif table.get(var1) and not table.get(var2):
    		var = self.buscaVariable(var1)
    		if var:
    			return var,var2
    		else:
    			print("Variable sin asignar  " + str(var1) + "  en la linea  " + str(self.instruction_pointer))
    			sys.exit(0)
    	elif not table.get(var1) and  table.get(var2):
    		var = self.buscaVariable(var2)
    		if var:
    			return var1,var
    		else:
    			print("Variable sin asignar  " + str(var2) + "  en la linea  " + str(self.instruction_pointer))
    			sys.exit(0)
    		var = self.buscaVariable(var2)
    		
    	elif table.get(var1) and table.get(var2):
    		var = self.buscaVariable(var1)
    		varx = self.buscaVariable(var2)
    		if var:
    			return var,varx
    		else:
    			print("Variable sin asignar  " + str(var1) + "  en la linea  " + str(self.instruction_pointer))
    			print("Variable sin asignar  " + str(var2) + "  en la linea  " + str(self.instruction_pointer))
    			sys.exit(0)

    def plus(self, quadruplo, table):
    	
    	op, oper1, oper2, var = quadruplo
    	# operando1, operando2 = self.getValores(oper1, oper2, table)
    	operando1 = self.buscaVariable(oper1)
    	operando2 = self.buscaVariable(oper2)
    	# print("mas", operando1)
    	# print("mas", operando2)
    	resultado = operando1+operando2
    	self.scope_stack.top().variables_scope[var]=resultado
        #self.push(self.pop() + self.pop())

    def exit(self):
        sys.exit(0)

    def minus(self, quadruplo, table):
    	
    	op, oper1, oper2, var = quadruplo
    	# operando1, operando2 = self.getValores(oper1, oper2, table)
    	# print(self.scope_stack.top().variables_scope)
    	operando1 = self.buscaVariable(oper1)
    	operando2 = self.buscaVariable(oper2)
    	# print("menos", operando1)
    	# print("menos", operando2)
    	resultado = operando1-operando2
    	self.scope_stack.top().variables_scope[var]=resultado

    def mul(self, quadruplo, table):
    	# print(self.scope_stack.top().variables_scope)
    	op, oper1, oper2, var = quadruplo
    	# operando1, operando2 = self.getValores(oper1, oper2, table)
    	operando1 = self.buscaVariable(oper1)
    	operando2 = self.buscaVariable(oper2)
    	# print("mul", operando1)
    	# print("mul", operando2)
    	resultado = operando1*operando2
    	self.scope_stack.top().variables_scope[var]=resultado

    def div(self, quadruplo, table):
    	
    	op, oper1, oper2, var = quadruplo
    	# operando1, operando2 = self.getValores(oper1, oper2, table)
    	operando1 = self.buscaVariable(oper1)
    	operando2 = self.buscaVariable(oper2)
    	# print("div", operando1)
    	# print("div", operando2)
    	resultado = operando1/operando2
    	self.scope_stack.top().variables_scope[var]=resultado

    def mod(self, quadruplo, table):
    	pass
        # last = self.pop()
        # self.push(self.pop() % last)

    def condicion(self, quadruplo, table):
        
        op, oper1, oper2, var = quadruplo
        # operando1, operando2 = self.getValores(oper1, oper2, table)
        operando1 = self.buscaVariable(oper1)
        operando2 = self.buscaVariable(oper2)
        # print("cond", operando1)
        # print("cond", operando2)
        for case in switch(op):
            if case('<'):
            	if operando1 < operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('>'):
            	if operando1 > operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('<='):
            	if operando1 <= operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('>='):
            	if operando1 >= operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('=='):
            	if operando1 == operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('!='):
            	if operando1 != operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('&&'):
            	if operando1 and operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case('||'):
            	if operando1 or operando2:
            		self.scope_stack.top().variables_scope[var]=True
            	else:
            		self.scope_stack.top().variables_scope[var]=False
            	break
            if case():
            	print("something else!")    	

    def dup(self):
        self.push(self.top())

    def over(self):
        b = self.pop()
        a = self.pop()
        self.push(a)
        self.push(b)
        self.push(a)

    def drop(self):
        self.pop()

    def swap(self):
        b = self.pop()
        a = self.pop()
        self.push(b)
        self.push(a)

    def print(self,quadruplo, table):
    	
    	escribe, num = quadruplo
    	param = self.code[self.instruction_pointer:self.instruction_pointer+num]
    	for item in param:
    		var = self.buscaVariable(item[1])
    		sys.stdout.write("escribe:  %s\n" % str(var))
    		sys.stdout.flush()
    	self.instruction_pointer = self.instruction_pointer+num	
    def println(self):
        sys.stdout.write("%s\n" % self.pop())
        sys.stdout.flush()

    def read(self):
        self.push(get_input())

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

    def eq(self):
        # self.push(self.pop() == self.pop())
        pass

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)

    def jmp(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")

    def dump_stack(self):
        print("\nstack", self.scope_stack.top().variables_scope)
        print("\nData stack (top first):")
        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))