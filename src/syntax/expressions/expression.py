from enum import Enum


class ExpressionTypes(Enum):
    VALUE = 0
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    MODULO = 5


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
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__parse()

    def __parse(self):
        for i, token in enumerate(self.__tokens):
            if token in self.expressionDict:
                self.type = self.expressionDict[token]
                self.a = Expression(self.__tokens[0:i])
                self.b = Expression(self.__tokens[i+1:len(self.__tokens)])
                return

        self.type = ExpressionTypes.VALUE
        self.a = self.__tokens[0]
        self.b = None

    def usesSingleValue(self):
        return self.b is None

    def toPython(self):
        if self.usesSingleValue():
            if self.type == ExpressionTypes.VALUE:
                return str(self.a)
        else:
            return f"({self.a.toPython()}){self.__expressionMap[self.type]}({self.b.toPython()})"
