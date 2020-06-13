class SetVariable:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def toPython(self):
        return f"{self.variable.literal} = {self.value}"
