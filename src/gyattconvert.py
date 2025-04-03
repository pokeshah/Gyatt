import json
import re
import argparse
import tokenize
from io import StringIO
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.json'), "r") as f:
    python_to_gyatt = json.load(f)  # Directly use the dictionary from JSON

def convert_to_gyatt(python_code):
    python_code = re.sub(r'print\((.*?)\)', r'yap about \1', python_code)

    tokens = list(tokenize.generate_tokens(StringIO(python_code).readline))
    for i, token in enumerate(tokens):
        token_str = token.string
        if token_str in python_to_gyatt:
            token_str = python_to_gyatt[token_str]
        tokens[i] = (token[0], token_str, token[2], token[3], token[4])
    gyatt_code = tokenize.untokenize(tokens)
    gyatt_code = re.sub(r":", " tho", gyatt_code)
    gyatt_code = re.sub(r"^(?!\s*$)(?!.*tho$).*", lambda m: m.group(0) + " rn", gyatt_code, flags=re.MULTILINE)
    return gyatt_code

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Python file to convert")
    parser.add_argument("out", nargs="?", help="File name to save the Gyatt code")
    args = parser.parse_args()
    if not args.file.endswith(".py"):
        print("Error: Input file must be a Python (.py) file")
        return
    with open(args.file, "r") as f:
        python_code = f.read()
    gyatt_code = convert_to_gyatt(python_code)
    output_file = args.out if args.out else args.file.replace(".py", ".gyt")
    if not output_file.endswith(".gyt"):
        output_file += ".gyt"
    with open(output_file, "w") as f:
        f.write(gyatt_code)
    print(f"Conversion complete! Gyatt file saved as: {output_file}")

if __name__ == "__main__":
    main()