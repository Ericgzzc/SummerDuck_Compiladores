import sys
import ply.yacc as yacc
from Parser import Parser
from Quads import*


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "prueba.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Parser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    lst = parser.parse(text,tracking=True)
    quad= Quads(lst)
    # print(lst)
    # print(quad.programa)
    # print(quad.nombre)
    # print(quad.dec_val)
    # print(quad.dec_fun)
    # print(quad.principal)


    # programa, nombre, dec_val, dec_fun, principal = lst;
