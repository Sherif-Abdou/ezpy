import sys
from os import path, getcwd

from src.Tokenizer import Tokenizer
from src.parser import Parser

if __name__ == "__main__":
    input_file = sys.argv[1]
    full_input_path = path.normpath(path.join(getcwd(), input_file))

    with open(full_input_path, "r") as file:
        text = file.read()
    tokenizer = Tokenizer(text)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    print(tree)
    # with open("../output_file.py", "w") as file:
    #     file.write(outputter.createPython())
