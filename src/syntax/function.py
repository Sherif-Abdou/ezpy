from src.syntax import Scope
import src.parser as parsers


class Function(Scope):
    def __init__(self, literal, tokens):
        self.literal = literal
        self.tokens = tokens
        super().__init__()
        self.__parse()

    def __parse(self):
        parser = parsers.Parser(self.tokens, self)
        self.commands = parser.parse()

    def toPython(self):
        newline = "\n    "
        if self.literal == "main":
            return f"""if __name__ == "__main__":{newline}{newline.join([command.toPython() for command in self.commands])}"""
