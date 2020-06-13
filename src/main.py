import sys
from os import path, getcwd

import src.Tokenizer
import src.builtin as builtin
from src.parser import Parser
import src.syntax as syntax

if __name__ == "__main__":
    input_file = sys.argv[1]
    full_input_path = path.normpath(path.join(getcwd(), input_file))

    with open(full_input_path, "r") as file:
        text = file.read()
    tokenizer = src.Tokenizer(text)
    tokens = tokenizer.tokenize()

    root_scope = syntax.Scope()
    root_scope.functions = builtin.map_python_functions()

    parser = Parser(tokens, scope=root_scope)
    tree = parser.parse()

    print(tree)
    # with open("../output_file.py", "w") as file:
    #     file.write(outputter.createPython())
