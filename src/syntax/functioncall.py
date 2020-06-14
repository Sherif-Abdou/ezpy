import src.syntax.expressions as expressions


class FunctionCall:
    def __init__(self, function, params):
        self.function = function
        self.params = params
        self.__parse()

    def __parse(self):
        commas = self.__find_commas()
        if not commas:
            self.params = [expressions.Expression(self.params)]
        else:
            split_params = self.__split_commas(commas)
            parsed_params = [expressions.Expression(tokens) for tokens in split_params]
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
