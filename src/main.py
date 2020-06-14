import sys
from os import path, getcwd

import src.Tokenizer
import src.builtin as builtin
from src.parser import Parser
import src.syntax as syntax
import src

if __name__ == "__main__":
    input_file = sys.argv[1]
    full_input_path = path.abspath(input_file)

    with open(full_input_path, "r") as file:
        text = file.read()
    tokenizer = src.Tokenizer(text)
    tokens = tokenizer.tokenize()

    root_scope = syntax.Scope()
    root_scope.functions = builtin.map_python_functions()

    parser = Parser(tokens, scope=root_scope)
    tree = parser.parse()

    python = src.create_python(tree)

    full_output_path = path.join(path.dirname(full_input_path), path.splitext(full_input_path)[0] + ".py")
    with open(full_output_path, "w") as file:
        file.write(python)
