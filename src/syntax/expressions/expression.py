from enum import Enum
import src.parser as parsers


class ExpressionTypes(Enum):
    VALUE = 0
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    MODULO = 5
    COMMAND = 6


class Expression:
    expressionDict = {
        "plus": ExpressionTypes.ADDITION,
        "minus": ExpressionTypes.SUBTRACTION,
        "times": ExpressionTypes.MULTIPLICATION,
        "over": ExpressionTypes.DIVISION,
        "mod": ExpressionTypes.MODULO
    }

    __expressionMap = {
        ExpressionTypes.ADDITION: "+",
        ExpressionTypes.SUBTRACTION: "-",
        ExpressionTypes.MULTIPLICATION: "*",
        ExpressionTypes.DIVISION: "/",
        ExpressionTypes.MODULO: "%"
    }

    def __init__(self, tokens, scope=None):
        self.__tokens = tokens
        self.scope = scope
        self.__parse()

    def __parse(self):
        for i, token in enumerate(self.__tokens):
            if token in self.expressionDict:
                self.type = self.expressionDict[token]
                self.a = Expression(self.__tokens[0:i])
                self.b = Expression(self.__tokens[i + 1:len(self.__tokens)])
                return

        possible_command = parsers.LineParser(self.__tokens, self.scope, True)
        if possible_command.parse() is not None:
            self.a = possible_command.parse()
            self.type = ExpressionTypes.COMMAND
        else:
            self.type = ExpressionTypes.VALUE
            self.a = self.__tokens[0]
        self.b = None

    def usesSingleValue(self):
        return self.b is None

    def toPython(self):
        if self.usesSingleValue():
            if self.type == ExpressionTypes.VALUE:
                return str(self.a)
            elif self.type == ExpressionTypes.COMMAND:
                return self.a.toPython()
        else:
            return f"({self.a.toPython()}){self.__expressionMap[self.type]}({self.b.toPython()})"
