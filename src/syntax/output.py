class Output:
    def __init__(self, value):
        self.value = value

    def toPython(self):
        return f"print({self.value.toPython()})"