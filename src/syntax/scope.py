from typing import List
import src.syntax as syntax


class Scope:
    def __init__(self):
        self.variables: List[syntax.Variable] = []
        self.functions: List[syntax.Function] = []
        self.commands = []
        self.parent: Scope = None

    def findVariable(self, literal):
        if self.parent and self.parent.findVariable(literal):
            return self.parent.findVariable(literal)
        for variable in self.variables:
            if variable.literal == literal:
                return variable

        return None

    def findFunction(self, literal):
        if self.parent and self.parent.findFunction(literal):
            return self.parent.findFunction(literal)
        for function in self.functions:
            if function.literal == literal:
                return function

        return None
