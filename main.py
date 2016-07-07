import sys
import ply.yacc as yacc
from Parser import Parser
from Quads import*
from mv import*
import re
import json 


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
    # print(lst)
    quad= Quads(lst)
    # print(quad.lista_quadruplos)
    # 

    try:
        if quad.error:
            filename2 = "codigoIntermedio.txt"
            file2 = open(filename2, "w")
        
            
            for item in quad.lista_quadruplos:
                json.dump(item, file2)
                file2.write("\n")
            file2.close()
            # with open(filename2) as f:
            #     content = f.read().splitlines()

            a = Machine(quad.lista_quadruplos)
            a.run()
            a.dump_stack()
        else:
            print("Error")
    except IOError:
            print("Cannot open {0} file2".format(filename2))
            sys.exit(0)
    except (RuntimeError, IndexError) as e:
            print("IndexError: %s" % e)
    except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

    # print(lst)
    # print(quad.programa)
    # print(quad.nombre)
    # print(quad.dec_val)
    # print(quad.dec_fun)
    # print(quad.principal)


    # programa, nombre, dec_val, dec_fun, principal = lst;
