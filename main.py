import TreePrinter
import sys
import Mparser
import scanner
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':
    # control_transfer
    # init
    # opers
    filename = sys.argv[1] if len(sys.argv) > 1 else "init.m"
    filename = "data/" + filename
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
        print('start TypeChecker')
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
        if typeChecker.error:
            sys.exit(1)  # if there was an error in TypeChecker there is no point in using Interpreter
        print('start Interpreter')
        ast.accept(Interpreter())
        # in future
        # ast.accept(OptimizationPass1())
        # ast.accept(OptimizationPass2())
        # ast.accept(CodeGenerator())
