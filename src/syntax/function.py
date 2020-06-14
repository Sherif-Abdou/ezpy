import src.parser as parsers
import src.syntax as syntax


class Function(syntax.Scope):
    def __init__(self, literal, tokens=[], param_tokens=[], parent=None, shouldParse=True):
        super().__init__()
        self.parent = parent
        self.literal = literal
        self.__tokens = tokens
        self.__param_tokens = param_tokens
        if shouldParse:
            self.__parse()
            self.__param_parse()

    def __parse(self):
        parser = parsers.Parser(self.__tokens, scope=self)
        self.commands = parser.parse()

    def __param_parse(self):
        if not self.__param_tokens:
            return

        commas = self.__find_commas()
        if not commas:
            variable = syntax.Variable(self.__param_tokens[0])
            self.variables.append(variable)
        else:
            split_commas = self.__split_commas(commas)
            [self.variables.append(syntax.Variable(literal[0])) for literal in split_commas]


    def __split_commas(self, commas):
        split_params = []
        prevComma = -1
        for comma in commas:
            split_params.append(self.__param_tokens[prevComma + 1:comma])
            prevComma = comma
        return split_params

    def __find_commas(self):
        commas = []
        for i, token in enumerate(self.__param_tokens):
            if token == ",":
                commas.append(i)
        return commas

    def toPython(self):
        newline = "\n    "
        if self.literal == "main":
            return f"""if __name__ == "__main__":{newline}{newline.join([command.toPython() for command in self.commands])}"""
        else:
            return f"""def {self.literal}():{newline}{newline.join([command.toPython() for command in self.commands])}"""
