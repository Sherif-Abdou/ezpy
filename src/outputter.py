def create_python(tree):
    return "\n\n".join([item.toPython() for item in tree])
