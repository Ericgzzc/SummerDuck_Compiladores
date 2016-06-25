import sys
import ply.yacc as yacc
from Parser import Parser


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "prueba.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Parser()
    parser = yacc.yacc(module=Parser)
