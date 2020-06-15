from enum import Enum
from src.syntax.expressions import Expression


class ConditionTypes(Enum):
    ISTRUE = 0
    ISFALSE = 1
    GREATER = 2
    LESSER = 3
    GREATEROREQUAL = 4
    LESSEROREQUAL = 5
    EQUAL = 6


class Condition:
    conditionDict = {
        "less": ConditionTypes.LESSER,
        "equal": ConditionTypes.EQUAL,
        "greater": ConditionTypes.GREATER
    }

    __conditionMap = {
        ConditionTypes.LESSER: "<",
        ConditionTypes.EQUAL: "==",
        ConditionTypes.GREATER: ">"
    }

    def __init__(self, tokens, scope=None):
        self.__tokens = tokens
        self.scope = scope
        self.__parse()

    def __parse(self):
        # Looks for condition keywords
        for i, token in enumerate(self.__tokens):
            if token == "is" and self.__tokens[i + 1] in ["less", "equal", "greater"] and self.__tokens[i + 2] in [
                "than", "to"]:
                # Parses expressions before and after the condition keywords
                first_tokens = self.__tokens[0:i]
                second_tokens = self.__tokens[i + 3:len(self.__tokens)]
                self.first_expression = Expression(first_tokens, self.scope)
                self.second_expression = Expression(second_tokens, self.scope)
                self.conditionType = self.conditionDict[self.__tokens[i + 1]]

    def usesSingleValue(self):
        return self.second_expression is None

    def toPython(self):
        if not self.usesSingleValue():
            return f"({self.first_expression.toPython()}){self.__conditionMap[self.conditionType]}({self.second_expression.toPython()})"
