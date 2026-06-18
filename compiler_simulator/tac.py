import re

def generate_TAC(code):

    tac = []

    match = re.search(r'(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)', code)

    if match:

        result = match.group(1)
        op1 = match.group(2)
        operator = match.group(3)
        op2 = match.group(4)

        tac.append(f"t1 = {op1} {operator} {op2}")
        tac.append(f"{result} = t1")

    else:
        tac.append("Simple assignment")

    return tac