import json
import re
import argparse
import tokenize
from io import StringIO
import untokenize
import uwuify
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.json'), "r") as f:
    mappings = json.load(f)
python_to_gyatt = mappings

gyatt_slang = {v: k for k, v in python_to_gyatt.items()}

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType("r"), help="Input file")
parser.add_argument("out", nargs="?", help="Compile and save the code into a Python script at PATH")
parser.add_argument("--nouwu", "-n", action="store_true", help="Disable uwuification of strings")
args = parser.parse_args()

def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())

def rncheck(code):
    lines = code.split("\n")
    for i, line in enumerate(lines, start=1):
        if line and "\u0023" in line:
            raise SyntaxError(f"Line {i}: No comments in your code")
        if line and not line.strip().endswith("tho") and not line.strip().endswith("rn"):
            raise SyntaxError(f"Line {i}: Each line must end with 'tho' or 'rn'")
    return code

def interpret(gyatt_code):
    gyatt_code = re.sub(r'\s*rn\s*$', '', gyatt_code, flags=re.MULTILINE)
    gyatt_code = gyatt_code.replace(" tho", ":")
    gyatt_code = re.sub(r'yap about (.*?)$', r'print(\1)', gyatt_code, flags=re.MULTILINE)
    gyatt_code = gyatt_code.replace("aint be", "!=")
    gyatt_code = gyatt_code.replace("skibidi?", "skibidi")

    tokens = list(tokenize.generate_tokens(StringIO(gyatt_code).readline))
    for i, token in enumerate(tokens):
        for slang, replacement in gyatt_slang.items():
            if token.string == slang:
                tokens[i] = (token[0], replacement, token[2], token[3], token[4])
            if token.type == tokenize.STRING and not args.nouwu:
                tokens[i] = (
                    token[0],
                    uwuify.uwu(uwuify.uwu(token.string, flags=(uwuify.YU | uwuify.STUTTER))[2:],
                               flags=(uwuify.YU | uwuify.STUTTER))[2:],
                    token[2],
                    token[3],
                    token[4]
                )

    python_code = untokenize.untokenize(tokens)
    return (
            "import ctypes, random; ctypes.string_at(0) if random.randint(1, 6) == 1 else None\n" + "x = bytearray(1024*1024*1000*16)\n" + python_code
    )

def check_for_comments(code):
    multi_line_comment = r'"""(.*?)"""|\'\'\'(.*?)\'\'\''
    if re.search(multi_line_comment, code, re.DOTALL):
        raise ValueError("Comments are prohibited in the code.")
    return code

nouwu = args.nouwu
with args.file as gyatt:
    python_code = interpret(rncheck(check_for_comments(gyatt.read())))

if args.out:
    output = f"{str(args.out)}.py"
    with open(output, "w") as py:
        py.write(python_code)
    run(output)
else:
    exec(python_code)