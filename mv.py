from __future__ import print_function
from collections import deque
from Symboltable import *
from io import StringIO
import sys
import tokenize
import re

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

class Machine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.return_stack = Stack()
        self.modulo_stack = Stack()
        self.instruction_pointer = 0
        self.code = code
        self.table = SymbolTable(None, 'global')
        self.operations = {
            "%":       		self.mod,
            "*":        	self.mul,
            "+":        	self.plus,
            "-":        	self.minus,
            "/":        	self.div,
            "==":       	self.eq,
            "=":       		self.asigna,
        }
        self.modulos = {
        	"programa": 	self.programa,
        	"principal": 	self.principal,
        	"modulo": 		self.modulo,
        }
        self.variables = {
 		  	"global": 		self.global1,
            "local": 		self.local,
            "param": 		self.param,
 		}

        self.dis_map = {
            "regresa": 		self.regresa,
            "principal": 	self.principal,
            "si":       	self.si,
            "end_si":       self.end_si,
            "repite":       self.repite,
            "hasta":       	self.hasta,
            "mientras":     self.mientras,
            "end_mientras":	self.end_mientras,
            "llamada":		self.llamada,
            "escribe":		self.print,
            "leer":     	self.read,
            "jmp":      	self.jmp,
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
            self.dispatch(opcode)

    def dispatch(self, quadruplo):
        
        quad1 = quadruplo.split(",")
        quad = []
        for item in quad1:
        	term = re.sub(r'["|\[|\]|]', '', item)
        	quad = quad + [term,]
        op = quad[0]
        print(quad)
        print(self.instruction_pointer)

        if op in self.operations:
            self.operations[op]()
        elif op in self.modulos:
        	self.modulos[op](quadruplo, self.table)
        elif op in self.variables:
        	self.variables[op](quadruplo, self.table)
        elif isinstance(op, int):
            self.push(op) # push numbers on stack
        elif isinstance(op, str) and op[0]==op[-1]=='"':
            self.push(op[1:-1]) # push quoted strings on stack
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    def programa(self, quadruplo, table):
        pass
    def global1(self, quadruplo, table): 
    	pass
    def modulo(self,quadruplo, table): 
        pass
    def local(self): 
        pass
    def param(self): 
        pass
    def regresa(self): 
        pass
    def principal(self): 
        pass
    def si(self): 
        pass
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
    def llamada(self): 
        pass
    def print(self): 
        pass
    def read(self): 
        pass
    def asigna(self):
        pass

    def plus(self):
        self.push(self.pop() + self.pop())

    def exit(self):
        sys.exit(0)

    def minus(self):
        last = self.pop()
        self.push(self.pop() - last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)

    def mod(self):
        last = self.pop()
        self.push(self.pop() % last)

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

    def print(self):
    	pass
        # sys.stdout.write(str(self.pop()))
        # sys.stdout.flush()

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
        print("Data stack (top first):")
        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))