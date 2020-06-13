from enum import Enum

from src.syntax.expressions import Expression


class ConditionTypes(Enum):
    ISTRUE=0
    ISFALSE=1
    GREATER=2
    LESSER=3
    GREATEROREQUAL=4
    LESSEROREQUAL=5
    EQUAL=6


class Condition:
    conditionDict = {
        "less": ConditionTypes.LESSER,
        "equal": ConditionTypes.EQUAL,
        "greater": ConditionTypes.GREATER
    }

    def __init__(self, tokens):
        self.__tokens = tokens
        self.__parse()

    def __parse(self):
        for i, token in enumerate(self.__tokens):
            if token == "is" and self.__tokens[i+1] in ["less", "equal", "greater"] and self.__tokens[i+2] in ["than", "to"]:
                first_tokens = self.__tokens[0:i]
                second_tokens = self.__tokens[i+3:len(self.__tokens)]
                self.first_expression = Expression(first_tokens)
                self.second_expression = Expression(second_tokens)
                self.conditionType = self.conditionDict[self.__tokens[i+1]]


    def usesSingleValue(self):
        return self.second_expression is None
