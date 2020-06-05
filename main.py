import TreePrinter
import sys
import Mparser
import scanner
from TypeChecker import TypeChecker

if __name__ == '__main__':
    # control_transfer
    # init
    # opers
    filename = sys.argv[1] if len(sys.argv) > 1 else "init.m"
    try:
        file = open(filename)
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)
    if ast:
        ast.printTree()
        print('start treewalk')
        typeChecker = TypeChecker()
        typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
