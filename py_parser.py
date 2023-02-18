def isblank(line):
    return len(line.strip()) == 0


def indent(line):
    cnt = 0
    for char in line:
        if char == " ":
            cnt += 1
        else:
            break
    return cnt


def is_assignment(tokens):
    if len(tokens) >= 3 and tokens[1] == "=":
        return True


def is_conditional(tokens):
    if len(tokens) >= 1 and tokens[0] in ("if", "elif", "else"):
        return True


def is_for_loop(tokens):
    if len(tokens) >= 1 and tokens[0] == "for":
        return True


def is_while_loop(tokens):
    if len(tokens) >= 1 and tokens[0] == "while":
        return True


def is_print(tokens):
    if len(tokens) >= 1 and tokens[0] == "print":
        return True


def is_input(tokens):
    if len(tokens) >= 1 and tokens[0] == "input":
        return True


def match_pattern(tokens):
    if is_assignment(tokens):
        return "ASSIGN"
    elif is_conditional(tokens):
        return "CONDITIONAL"
    elif is_for_loop(tokens):
        return "FOR"
    elif is_while_loop(tokens):
        return "WHILE"
    elif is_print(tokens):
        return "PRINT"
    elif is_input(tokens):
        return "INPUT"


def get_type(char):
    if char.isalpha():
        tp = "str"
    elif char.isdigit():
        tp = "num"
    else:
        tp = "sym"
    return tp


def tokenize(line):
    line = line.strip()
    token = []
    i = 0
    while i < len(line):
        char = line[i]
        if char in ["'", '"']:
            j = i
            i += 1
            while i < len(line):
                if line[i] == char:
                    break
                i += 1
            else:
                raise Exception(f"Unterminated string > {line}")

            token.append(line[j:i+1])
        elif char in [" ", "\t"]:
            i += 1
            continue
        else:
            cur = []
            current_type = get_type(char)

            while i < len(line):
                char = line[i]
                if char in [" ", "\n", "\t"]:
                    break
                elif char in ["'", '"']:
                    i -= 1
                    break
                elif get_type(char) != current_type:
                    i -= 1
                    break
                cur.append(char)
                i += 1

            while "(" in cur:
                cur.remove("(")
            while ")" in cur:
                cur.remove(")")

            cur = "".join(cur)
            if cur.isnumeric():
                token.append(int(cur))
            else:
                token.append(cur)
        i += 1

    tokens = []
    for t in token:
        if not isblank(str(t)) and t not in [",", ":"]:
            tokens.append(t)

    return tokens
