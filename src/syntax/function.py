import src.parser as parsers
import src.syntax as syntax


# Represents a function
class Function(syntax.Scope):
    def __init__(self, literal, tokens=[], param_tokens=[], parent=None, shouldParse=True):
        super().__init__()
        self.parent = parent
        self.literal = literal
        self.params = []
        self.__tokens = tokens
        self.__param_tokens = param_tokens
        if shouldParse:
            self.__parse()
            self.__param_parse()

    def __parse(self):
        parser = parsers.Parser(self.__tokens, scope=self)
        self.commands = parser.parse()

    # Parses function parameters
    def __param_parse(self):
        if not self.__param_tokens:
            return

        commas = self.__find_commas()
        if not commas:
            # Group all the tokens as one parameter if there's no commas
            variable = syntax.Variable(self.__param_tokens[0], None)
            self.params.append(variable)
            self.variables.append(variable)
        else:
            # Splits the tokens around the commas and parses each parameter
            split_commas = self.__split_commas(commas)
            for literal in split_commas:
                variable = syntax.Variable(literal[0], None)
                self.params.append(variable)
                self.variables.append(variable)

    # Splits parameter tokens based on commas
    def __split_commas(self, commas):
        split_params = []
        prevComma = -1
        for comma in commas:
            split_params.append(self.__param_tokens[prevComma + 1:comma])
            prevComma = comma
        split_params.append(self.__param_tokens[prevComma + 1:len(self.__param_tokens)])
        return split_params

    # Finds all comma tokens in the parameter tokens
    def __find_commas(self):
        commas = []
        for i, token in enumerate(self.__param_tokens):
            if token == ",":
                commas.append(i)
        return commas

    def toPython(self):
        newline = "\n    "
        param_strings = ", ".join([variable.literal for variable in self.params])
        if self.literal == "main":
            return f"""if __name__ == "__main__":{newline}{newline.join([command.toPython() for command in self.commands])}"""
        else:
            return f"""def {self.literal}({param_strings}):{newline}{newline.join([command.toPython() for command in self.commands])}"""
