import re


class Tokenizer:
    __words = r"([a-zA-Z_]+(?=(\n)|\s|($)|.|,)|\d+\.?\d*|(?<=[a-zA-Z_])\.(?=[a-zA-Z_])|,|(\".*\")|(\n))"

    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def tokenize(self):
        stripped_text = re.findall(self.__words, self.raw_text)
        stripped_text = self.__merge_capture_groups(stripped_text)
        print(stripped_text)
        return stripped_text

    def __merge_capture_groups(self, stripped_text):
        flattened = []
        for group in stripped_text:
            flattened.append(group[0])

        return flattened
