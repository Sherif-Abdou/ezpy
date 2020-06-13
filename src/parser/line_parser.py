import src.syntax as syntax


class LineParser:
    def __init__(self, tokens, scope):
        self.tokens = tokens
        self.scope = scope

    def parse(self):
        first = self.tokens[0]
        if first == "set" and self.tokens[2] == "to":
            literal = self.tokens[1]
            variable = self.scope.findVariable(literal)
            if variable is None:
                variable = syntax.Variable(literal, self.tokens[3])
                self.scope.variables.append(variable)

            return syntax.SetVariable(variable, self.tokens[3])
