from typing import List
from copy import deepcopy

from .line_parser import LineParser
from src.syntax.conditions import IfCondition
import src.syntax as syntax


class Parser():
    def __init__(self, tokens, scope=None, start=0, end=None):
        self.tokens: List[str] = deepcopy(tokens)
        self.start = start
        self.end = end
        self.scope = scope

        # Removes any trailing whitespace
        while True and len(self.tokens) != 0:
            last_index = len(self.tokens) - 1
            if self.tokens[last_index] != "\n":
                break
            del self.tokens[last_index]

        if self.end is None:
            self.end = len(self.tokens)

    # Finds the tokens of a start-end scope
    def __find_scope(self, start_token):
        first_start = self.tokens.index("start", start_token) + 1
        index = first_start

        # uses i to represent sub scopes and to not count them
        i = 0
        while index < len(self.tokens):
            if self.tokens[index] == "end":
                if i == 0:
                    return first_start, index
                else:
                    i -= 1

            if self.tokens[index] == "start":
                i += 1

            index += 1

    def parse(self):
        lines = self.__find_newlines(self.start, self.end)
        commands = []
        index = self.start
        while index < len(lines) - 1:
            # Sees if a token represents a scope command
            token_index = lines[index] + 1
            scope_command = self.__find_scope_command(token_index)
            if scope_command is not None:
                # Adds scoped command to commands and moves index to after the parsed scope
                index = self.__next_newline(lines, scope_command[1])
                commands.append(scope_command[0])
                continue
            else:
                # Gets a subarray of the line's tokens
                start = lines[index] + 1
                end = lines[index + 1]
                if not self.tokens[start:end]:
                    index += 1
                    continue
                # Inputs the subarray to LineParser for further parsing
                line_parser = LineParser(self.tokens[start:end], self.scope)
                commands.append(line_parser.parse())

            index += 1

        return commands

    # Checks for any commands that create a new scope(ex functions, if statements)
    def __find_scope_command(self, start):
        if self.tokens[start] == "func":
            start_end = self.__find_scope(start)
            params_tokens = self.tokens[start+2:start_end[0]-1]
            function = syntax.Function(self.tokens[start + 1], self.__token_subset(start_end), param_tokens=params_tokens, parent=self.scope)
            self.scope.functions.append(function)
            return function, start_end[1] + 1
        elif self.tokens[start] == "if":
            start_end = self.__find_scope(start)
            condition_tokens = self.tokens[start + 1: start_end[0] - 1]
            if_condition = IfCondition(condition_tokens, self.__token_subset(start_end), super_scope=self.scope)
            return if_condition, start_end[1] + 1
        return None

    # Turns a start-end tuple to a subarray
    def __token_subset(self, start_end):
        return self.tokens[start_end[0] + 1:start_end[1]]

    # Look for all newlines(\n) in the token array
    def __find_newlines(self, start, end):
        newlines = [start - 1] + [i for i, j in enumerate(self.tokens) if j == "\n"]
        newlines = [i for i in newlines if (start - 1) <= i < end] + [end]
        return newlines

    # Finds the next newline starting at an token index
    def __next_newline(self, newlines: List[str], index: int):
        for i, newline in enumerate(newlines):
            if newline >= index:
                return i
        return len(newlines)
