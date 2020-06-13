from typing import List
import src.parser as parsers
from src.syntax.conditions import Condition
from src.syntax import Scope


class IfCondition(Scope):
    def __init__(self, condition_tokens: List[str], body_tokens: List[str], super_scope: Scope=None):
        super().__init__()
        self.parent = super_scope
        self.__condition_tokens = condition_tokens
        self.__body_tokens = body_tokens
        if self.__body_tokens[len(self.__body_tokens) - 1] == "\n":
            del self.__body_tokens[len(self.__body_tokens) - 1]
        self.condition = Condition(self.__condition_tokens)
        self.__parse()

    def __parse(self):
        newlines = self.__find_newlines(0, len(self.__body_tokens))
        parser = parsers.Parser(self.__body_tokens)
        for i, newline in enumerate(newlines):
            token = self.__body_tokens[newline + 1]
            if token == "else":
                main_body = self.__body_tokens[0:newlines[i]]
                main_parser = parsers.Parser(main_body, scope=self)
                sub = self.__body_tokens[newlines[i + 1]: len(self.__body_tokens)]
                sub_parser = parsers.Parser(main_body, scope=self)
                self.main_commands = main_parser.parse()
                self.else_commands = sub_parser.parse()
                return

        self.main_commands = parser.parse()
        return

    def __find_newlines(self, start, end):
        newlines = [start - 1] + [i for i, j in enumerate(self.__body_tokens) if j == "\n"]
        newlines = [i for i in newlines if (start - 1) <= i < end]
        return newlines
