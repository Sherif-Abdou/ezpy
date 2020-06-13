import src.syntax as syntax


def map_python_functions():
    print = syntax.Function("print", shouldParse=False)

    return [print]
