from typing import List
from .variable import Variable


class Scope:
    def __init__(self):
        self.variables: List[Variable] = []
        self.commands = []
        self.parent: Scope = None

    def findVariable(self, literal):
        if self.parent and self.parent.findVariable(literal):
            return self.parent.findVariable(literal)
        for variable in self.variables:
            if variable.literal == literal:
                return variable

        return None
