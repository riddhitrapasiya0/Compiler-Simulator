import re

def lexer(code):

    pattern = r'[A-Za-z_]+|\d+|==|=|\+|\-|\*|\/|\(|\)|;'

    words = re.findall(pattern, code)

    tokens = []

    for w in words:

        if w in ["int","float","if","else","while"]:
            tokens.append(("KEYWORD", w))

        elif w.isdigit():
            tokens.append(("NUMBER", w))

        elif w in "+-*/=":
            tokens.append(("OPERATOR", w))

        elif w == ";":
            tokens.append(("SEMICOLON", w))

        else:
            tokens.append(("IDENTIFIER", w))

    return tokens