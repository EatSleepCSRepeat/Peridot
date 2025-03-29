import sys
import os
import shlex
import re

def MatchVariable(s):
    s = re.sub(r'$.*$', '', s)
    tokens = [match.group(0) for match in re.finditer(r'(\".*?\"|\'.*?\'|\S+)', s)]
    parsed_tokens = []
    for token in tokens:
        if token.startswith("'") and token.endswith("'") or token.startswith('"') and token.endswith('"'):
            parsed_tokens.append(token[1:-1]) 
        elif token.isdigit():
            parsed_tokens.append(int(token)) 
        else:
            parsed_tokens.append(token)
    return parsed_tokens

def Resolve(text, variables):
    def replace(match):
        var_name = match.group(1)
        value = variables.get(var_name)
        if value is None:
            return match.group(0) 
        return str(value)

    return re.sub(r'\${(\w+)}', replace, text)

def Display(tokens, variables):
    if len(tokens) > 1:
        resolved = Resolve(tokens[1], variables)

        if re.search(r'\${(\w+)}', resolved):
            for name in variables:
                value = variables[name]
                if isinstance(value, int) and any(c.isalpha() for c in resolved):
                    print(f"?error: can't concatenate int with string (variable '{name}' is an int)")
                    return
                if isinstance(value, str) and resolved.isdigit():
                    print(f"?error: can't concatenate string with int (variable '{name}' is a string)")
                    return
        
        print(resolved)
    else:
        print("?error: missing argument for display")

variables = {}
sys.argv = sys.argv[1:]

if len(sys.argv) >= 1:
    try:
        sys.argv[0] = str(sys.argv[0])
    except Exception as e:
        print("?error: " + str(e).lower())
        sys.exit(1)

    if os.path.exists(sys.argv[0]):
        with open(sys.argv[0], 'r') as f:
            for line in f.readlines():
                line = line.strip()

                if not line or line.startswith('$'):
                    continue

                try:
                    tokens = MatchVariable(line)
                except ValueError as e:
                    print(f"?error: {e}")
                    sys.exit(1)

                if not tokens:
                    continue

                command = tokens[0]

                match command:
                    case 'display':
                        Display(tokens, variables)

                    case 'newline':
                        try:
                            newlineamt = int(shlex.split(line)[1])
                        except Exception as e:
                            print("?error: " + str(e).lower())
                            sys.exit(1)
                            
                        for i in range(newlineamt):
                            print()
                    case _ if len(tokens) >= 3 and tokens[1] == "=":
                        name = tokens[0]
                        value = " ".join(tokens[2:]) if isinstance(tokens[2], str) else tokens[2]
                        variables[name] = value

                    case _:
                        print(f"?error: unknown statement or variable {command}")
                        sys.exit(1)
    else:
        print("?error: file selected does not exist")
        sys.exit(1)
