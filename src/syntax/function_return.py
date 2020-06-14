import src.syntax.expressions as expressions


class Return:
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__parse()

    def __parse(self):
        self.return_expression = expressions.Expression(self.__tokens)

    def toPython(self):
        return f"""return {self.return_expression.toPython()}"""
