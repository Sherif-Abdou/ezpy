import src.syntax as syntax


# Maps builtin python functions to ezpy functions
def map_python_functions():
    print = syntax.Function("print", shouldParse=False)
    round = syntax.Function("round", shouldParse=False)

    return [print, round]
