import src.syntax as syntax


class LineParser:
    def __init__(self, tokens, scope, inline=False):
        self.tokens = tokens
        self.scope = scope
        self.inline = inline

    def parse(self):
        first = self.tokens[0]
        if not self.inline and first == "set" and self.tokens[2] == "to":
            literal = self.tokens[1]
            variable = self.scope.findVariable(literal)
            if variable is None:
                variable = syntax.Variable(literal, self.tokens[3])
                self.scope.variables.append(variable)

            return syntax.SetVariable(variable, self.tokens[3])
        elif self.scope:
            literal = self.scope.findFunction(self.tokens[0])
            if literal is None:
                return None
            command = syntax.FunctionCall(literal, self.tokens[1:len(self.tokens)], self.scope)
            return command

        return None
