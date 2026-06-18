def semantic(code):

    if "b" in code and "int b" not in code:
        return "❌ Semantic Error: variable b not declared"

    return "✔ Semantic Analysis Passed"