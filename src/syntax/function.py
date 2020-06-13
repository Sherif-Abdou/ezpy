import src.parser as parsers
import src.syntax as syntax


class Function(syntax.Scope):
    def __init__(self, literal, tokens=[], parent=None, shouldParse=True):
        super().__init__()
        self.parent = parent
        self.literal = literal
        self.__tokens = tokens
        if shouldParse:
            self.__parse()

    def __parse(self):
        parser = parsers.Parser(self.__tokens, scope=self)
        self.commands = parser.parse()

    def toPython(self):
        newline = "\n    "
        if self.literal == "main":
            return f"""if __name__ == "__main__":{newline}{newline.join([command.toPython() for command in self.commands])}"""
