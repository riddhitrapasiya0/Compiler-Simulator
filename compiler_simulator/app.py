from flask import Flask, render_template, request
import re

app = Flask(__name__)

# ---------------- LEXICAL ANALYSIS ----------------
def lexer(code):

    pattern = r'[A-Za-z_][A-Za-z0-9_]*|\d+|==|=|\+|\-|\*|\/|;'
    words = re.findall(pattern, code)

    tokens = []

    for w in words:

        if w.isdigit():
            tokens.append(("NUMBER", w))

        elif w in "+-*/=":
            tokens.append(("OPERATOR", w))

        elif w == ";":
            tokens.append(("SEMICOLON", w))

        else:
            tokens.append(("IDENTIFIER", w))

    return tokens


# ---------------- SYNTAX ANALYSIS ----------------
def syntax_analysis(code):

    lines = code.split("\n")
    errors = []

    # ✅ numbers + variables allowed
    pattern = r'^[a-zA-Z]+\s*=\s*([a-zA-Z]+|\d+)\s*[\+\-\*/]\s*([a-zA-Z]+|\d+)\s*;$'

    for i, line in enumerate(lines, start=1):

        line = line.strip()

        if line == "":
            continue

        if not re.match(pattern, line):
            errors.append(f"Syntax Error in line {i}: {line}")

    if errors:
        return ", ".join(errors)

    return "Syntax Correct"


# ---------------- SEMANTIC ANALYSIS ----------------
def semantic_analysis(code):

    lines = code.split("\n")
    defined_vars = set()

    for i, line in enumerate(lines, start=1):

        line = line.strip()

        if line == "":
            continue

        match = re.match(
            r'([a-zA-Z]+)\s*=\s*([a-zA-Z]+|\d+)\s*([\+\-\*/])\s*([a-zA-Z]+|\d+);',
            line
        )

        if not match:
            return f"Semantic Error in line {i}"

        result = match.group(1)
        op1 = match.group(2)
        op2 = match.group(4)

        # ✅ check operands
        if not op1.isdigit() and op1 not in defined_vars:
            return f"Semantic Error: '{op1}' used before declaration (line {i})"

        if not op2.isdigit() and op2 not in defined_vars:
            return f"Semantic Error: '{op2}' used before declaration (line {i})"

        # ✅ mark result variable as defined
        defined_vars.add(result)

    return "Semantic Correct"


# ---------------- 3 ADDRESS CODE ----------------
def generate_TAC(code):

    tac = []
    temp = 1

    lines = code.split("\n")

    for line in lines:

        match = re.search(
            r'(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)',
            line
        )

        if match:

            result = match.group(1)
            op1 = match.group(2)
            operator = match.group(3)
            op2 = match.group(4)

            tac.append(f"t{temp} = {op1} {operator} {op2}")
            tac.append(f"{result} = t{temp}")

            temp += 1

    return tac


# ---------------- PARSE TREE ----------------
def parse_trees(code):

    trees = []

    lines = code.split("\n")

    for line in lines:

        match = re.search(
            r'(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)',
            line
        )

        if match:

            trees.append({
                "result": match.group(1),
                "operator": match.group(3),
                "op1": match.group(2),
                "op2": match.group(4)
            })

    return trees


# ---------------- MAIN ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():

    code = ""
    tokens = []
    syntax = ""
    semantic = ""
    tac = []
    trees = []

    if request.method == "POST":

        code = request.form["code"]

        tokens = lexer(code)
        syntax = syntax_analysis(code)
        semantic = semantic_analysis(code)
        tac = generate_TAC(code)
        trees = parse_trees(code)

    return render_template(
        "index.html",
        code=code,
        tokens=tokens,
        syntax=syntax,
        semantic=semantic,
        tac=tac,
        trees=trees
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)