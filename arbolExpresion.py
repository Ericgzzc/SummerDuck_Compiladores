import re, string
Inputbuf = []

def gettoken(): 
	global Inputbuf

	p = re.search('^\W*[\+\-\*/]|^\W*[0-9]+', Inputbuf)
	token = p.string[p.regs[0][0]:p.regs[0][1]]

	if token not in ['+', '-', '*', '/']:
		token = int(token)
	Inputbuf = Inputbuf[p.regs[0][1]:]
	return token
	

# lookahead() peeks into the input stream and tells you what
# the next input token is
	
def lookahead():
	global Inputbuf
	try:
		p = re.search('^\W*[\+\-\*/]|^\W*[0-9]+', Inputbuf)
		token = p.string[p.regs[0][0]:p.regs[0][1]]
		if token not in ['+', '-', '*', '/']:
			token = int(token)
		return token
	except:
		return None
	
class Tree:
	pass
	
def factor():
	newnode = Tree()
	newnode.number = gettoken()
	newnode.left = newnode.right = 0
	return newnode
	
def term():
	left = factor()
	tmp = lookahead()
	while (tmp in ['*', '/']):
		gettoken()
		right = factor()
		newnode = Tree()
		newnode.op = tmp
		newnode.left = left
		newnode.right = right
		left = newnode
		tmp = lookahead()

	return left
	
def expression():
	left = term()
	tmp = lookahead()	
	while (tmp in ['+', '-']):
		gettoken()
		right = term()
		newnode = Tree()
		newnode.op = tmp
		newnode.left = left
		newnode.right = right
		left = newnode
		tmp = lookahead()
	
	return left
	
def treeprint(ptree):
	if (ptree):
		try:
			print(ptree.op)
		except:
			print(ptree.number)
		treeprint(ptree.left)
		treeprint(ptree.right)
		
def main():
	global Inputbuf
	Inputbuf = input()
	ptree = expression()
	return ptree
	
if __name__=='__main__':
	ptree = main()
	treeprint(ptree)