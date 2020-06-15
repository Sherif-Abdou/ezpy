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
        # Trims trailing whitespace
        if self.__body_tokens[len(self.__body_tokens) - 1] == "\n":
            del self.__body_tokens[len(self.__body_tokens) - 1]
        self.condition = Condition(self.__condition_tokens, self.parent)
        self.__parse()

    def __parse(self):
        newlines = self.__find_newlines(0, len(self.__body_tokens))
        parser = parsers.Parser(self.__body_tokens)
        for i, newline in enumerate(newlines):
            token = self.__body_tokens[newline + 1]
            # Parse if and else bodies separately if there's an else present
            if token == "else":
                main_body = self.__body_tokens[0:newlines[i]]
                main_parser = parsers.Parser(main_body, scope=self)
                sub = self.__body_tokens[newlines[i + 1]: len(self.__body_tokens)]
                sub_parser = parsers.Parser(sub, scope=self)
                self.main_commands = main_parser.parse()
                self.else_commands = sub_parser.parse()
                return

        # If there's no else, parse the entire body as one
        self.main_commands = parser.parse()
        return

    # Finds all newlines in the token array
    def __find_newlines(self, start, end):
        # Adds the beginning index to the array so parsing starts at the beginning
        # token instead of the first newline
        newlines = [start - 1] + [i for i, j in enumerate(self.__body_tokens) if j == "\n"]
        newlines = [i for i in newlines if (start - 1) <= i < end]
        return newlines

    def toPython(self):
        tab = "    "
        newline = f"\n{tab*self.parentCount()}"
        else_newline = f"\n{tab*(self.parentCount()-1)}"
        string = f"""if {self.condition.toPython()}:{newline}{newline.join([command.toPython() for command in self.main_commands])}"""
        if self.else_commands is not None:
            elseString = f"""{else_newline}else:{newline}{newline.join([command.toPython() for command in self.else_commands])}"""
            string += elseString
        return string
