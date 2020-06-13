class Variable:
    def __init__(self, literal, value):
        self.literal = literal
        self.value = value

    def toPython(self):
        return str(self.literal)
