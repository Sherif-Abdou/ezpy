import src.syntax.expressions as expressions


class FunctionCall:
    def __init__(self, function, params, scope=None):
        self.function = function
        self.params = params
        self.scope = scope
        self.__parse()

    def __parse(self):
        if not self.params:
            self.params = []
            return
        commas = self.__find_commas()
        if not commas:
            self.params = [expressions.Expression(self.params, self.scope)]
        else:
            split_params = self.__split_commas(commas)
            parsed_params = [expressions.Expression(tokens, self.scope) for tokens in split_params]
            self.params = parsed_params

    def __split_commas(self, commas):
        split_params = []
        prevComma = -1
        for comma in commas:
            split_params.append(self.params[prevComma + 1:comma])
            prevComma = comma
        return split_params

    def __find_commas(self):
        commas = []
        for i, token in enumerate(self.params):
            if token == ",":
                commas.append(i)
        return commas

    def toPython(self):
        string_params = ",".join([expression.toPython() for expression in self.params])
        return f"{self.function.literal}({string_params})"
