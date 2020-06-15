import src.syntax as syntax
import src.syntax.expressions as expressions


class LineParser:
    def __init__(self, tokens, scope, inline=False):
        self.tokens = tokens
        self.scope = scope
        # Whether or not to check for only inline commands
        self.inline = inline

    def parse(self):
        first = self.tokens[0]
        if not self.inline and first == "set" and self.tokens[2] == "to":
            literal = self.tokens[1]
            variable = self.scope.findVariable(literal)
            value = expressions.Expression(self.tokens[3:len(self.tokens)], scope=self.scope)
            # If the variable isn't already in scope, add it in scope
            if variable is None:
                variable = syntax.Variable(literal, value)
                self.scope.variables.append(variable)

            return syntax.SetVariable(variable, value)
        elif not self.inline and first == "return":
            # Grabs all tokens after the return and passes it on for further parsing
            tokens = self.tokens[1:len(self.tokens)]
            command = syntax.Return(tokens)
            return command
        # Checks if the command is calling a function
        elif self.scope:
            literal = self.scope.findFunction(self.tokens[0])
            if literal is None:
                return None
            command = syntax.FunctionCall(literal, self.tokens[1:len(self.tokens)], self.scope)
            return command

        return None
