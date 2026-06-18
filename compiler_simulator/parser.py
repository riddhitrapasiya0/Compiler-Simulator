def parser(code):

    if ";" not in code:
        return "❌ Syntax Error: Missing semicolon"

    if "=" not in code:
        return "❌ Syntax Error: Assignment operator missing"

    return "✔ Syntax Correct"