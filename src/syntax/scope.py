from typing import List
import src.syntax as syntax


# A stack scope that holds variables and functions
class Scope:
    def __init__(self):
        self.variables: List[syntax.Variable] = []
        self.functions: List[syntax.Function] = []
        self.commands = []
        self.parent: Scope = None

    # Looks for a variable with a literal within the scope's variables or the parent's scope's variable
    def findVariable(self, literal):
        if self.parent and self.parent.findVariable(literal):
            return self.parent.findVariable(literal)
        for variable in self.variables:
            if variable.literal == literal:
                return variable

        return None

    # Looks for a function with a literal within the scope's functions or the parent's scope's function
    def findFunction(self, literal):
        if self.parent and self.parent.findFunction(literal):
            return self.parent.findFunction(literal)
        for function in self.functions:
            if function.literal == literal:
                return function

        return None

    # Counts how many parent scopes a scope has(used for python indentation)
    def parentCount(self):
        i = 1
        parent = self.parent
        if parent:
            i+=1
            parent = parent.parent

        return i
