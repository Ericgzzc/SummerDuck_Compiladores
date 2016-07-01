import re, string

class Tree:
	pass
	
class arbolExpresion(object):

	def __init__(self,input1):
		self.Inputbuf = input1

	def gettoken(self):

		p = re.search('^\W*[\+\-\*\<\>\==\/]|^\W*[a-zA-Z_][a-zA-Z0-9_]*|^\W*[\d\.\d]+', self.Inputbuf)
		if(p):
			try:
				token = float(p1.group())
			except:
				try:
					token = int(p1.group())
				except:
					token = p.group()
	
		self.Inputbuf = self.Inputbuf[len(token):]
		return token
		

	# self.lookahead() peeks into the input stream and tells you what
	# the next input token is
		
	def lookahead(self):
		try:
			p = re.search('^\W*[\+\-\*\<\>\==\/]|^\W*[a-zA-Z_][a-zA-Z0-9_]*|^\W*[\d\.\d]+', self.Inputbuf)
			if(p):
				try:
					token = float(p1.group())
				except:
					try:
						token = int(p1.group())
					except:
						token = p.group()
			return token
		except:
			return None
		

	def factor(self):
		newnode = Tree()
		tmp = self.gettoken()
		newnode.number = tmp
		newnode.data = tmp
		newnode.left = newnode.right = 0
		return newnode
		
	def term(self):
		left = self.factor()
		tmp = self.lookahead()
		while (tmp in ['*', '/']):
			self.gettoken()
			right = self.factor()
			newnode = Tree()
			newnode.data = tmp
			newnode.op = tmp
			newnode.left = left
			newnode.right = right
			left = newnode
			tmp = self.lookahead()

		return left
		
	def expression(self):
		lista = []
		while self.Inputbuf:
			lista+=self.gettoken()
		
		return lista

	def condicion(self):
		pass

	def treeprint(self,ptree):
		if(ptree):
			try:
				print(ptree.op)
			except:
				print(ptree.number)
			self.treeprint(ptree.left)
			self.treeprint(ptree.right)

	# def main():
	# 	input_ = input()
	# 	main = arbolExpresion(input_)
	# 	ptree = expression(main)
	# 	return ptree
		
	# if __name__=='__main__':
	# 	ptree = main()
	# 	treeprint(ptree)