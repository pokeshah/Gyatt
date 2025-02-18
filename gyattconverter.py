import re
import argparse
import tokenize
from io import StringIO

# Reverse of gyatt_slang for conversion from Python to Gyatt
python_to_gyatt = {
    "None": "rizz",
    "False": "cap",
    "True": "nocap",
    "and": "btw",
    "as": "like",
    "assert": "skibidi",
    "break": "stawp",
    "continue": "period",
    "def": "gyatt",
    "elif": "hawktuah",
    "else": "tuah",
    "except": "boom",
    "finally": "frfr",
    "for": "iveplayedthesegamesbefore",
    "from": "aldi",
    "if": "hawk",
    "import": "propertyinegypt",
    "==": "be",
    "lambda": "huzz",
    "nonlocal": "nogatekeep",
    "global": "nogatekeepfrfr",
    "not": "aint",
    "or": "idk",
    "pass": "idc",
    "raise": "lowtaperfade",
    "return": "yeet",
    "try": "choppedchin",
    "while": "yapuntil",
    "yield": "chill",
    "math": "nerd",
    "=": "finna",
    "range": "times",
    "+": "sigma"
}

def convert_to_gyatt(python_code):
    tokens = list(tokenize.generate_tokens(StringIO(python_code).readline))
    gyatt_code = ""
    
    for i, token in enumerate(tokens):
        token_str = token.string
        if token_str in python_to_gyatt:
            token_str = python_to_gyatt[token_str]
        tokens[i] = (token[0], token_str, token[2], token[3], token[4])
    
    gyatt_code = tokenize.untokenize(tokens)
    
    gyatt_code = re.sub(r":", " tho", gyatt_code)  # Convert colons to "tho"
    gyatt_code = re.sub(r"^(?!\s*$)(?!.*tho$).*", lambda m: m.group(0) + " rn", gyatt_code, flags=re.MULTILINE)  # Ensure lines that aren't empty a don't end with "tho" end with "rn"
    
    return gyatt_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Python file to convert")
    args = parser.parse_args()
    
    input_file = args.file
    if not input_file.endswith(".py"):
        print("Error: Input file must be a Python (.py) file")
        return
    
    with open(input_file, "r") as f:
        python_code = f.read()
    
    gyatt_code = convert_to_gyatt(python_code)
    
    output_file = input_file.replace(".py", ".gyt")
    with open(output_file, "w") as f:
        f.write(gyatt_code)
    
    print(f"Conversion complete! Gyatt file saved as: {output_file}")


if __name__ == "__main__":
    main()
