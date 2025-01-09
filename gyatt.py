import re
import argparse
import os
import tokenize
from io import StringIO
import untokenize  # use untokenize module because it gives normal output unlike tokenize module
import uwuify
import ast


gyatt_slang = {
    "rizz": "None",
    "cap": "False",  # cap synonymous to lrizz
    "nocap": "True",  # nocap synonymous to wrizz
    "btw": "and",
    "like": "as",
    "skibidi": "assert",
    "stawp": "break",
    "period": "continue",
    "gyatt": "def",
    "hawktuah": "elif",
    "tuah": "else",
    "boom": "except",
    "frfr": "finally",
    "iveplayedthesegamesbefore": "for",
    "aldi": "from",
    "hawk": "if",
    "propertyinegypt": "import",
    "be": "==",
    "huzz": "lambda",
    "nogatekeep": "nonlocal",
    "nogatekeepfrfr": "global",
    "aint": "not",
    "idk": "or",
    "idc": "pass",
    "lowtaperfade": "raise",
    "yeet": "return",
    "choppedchin": "try",
    "yapuntil": "while",
    "chill": "yield",
    "nerd": "math",
    "finna": "=",
    "rn": "",
    "tho": "\abcdefgh:",  # avoid hitting non-code
    "sigma": "+",
    "times": "range",
}

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType("r"), help="Input file")
parser.add_argument(
    "out", nargs="?", help="Compile and save the code into a Python script at PATH"
)
parser.add_argument(
    "--nouwu", "-n", action="store_true", help="Disable uwuification of strings"
)
args = parser.parse_args()


def run(runfile):
    """Runs the compiled Python code"""
    with open(runfile, "r") as rnf:
        exec(rnf.read())


def rncheck(code):
    """Checks if each line ends with 'tho' or 'rn'"""
    lines = code.split("\n")
    for i, line in enumerate(lines, start=1):
        if (
            line
            and not line.strip().endswith("tho")
            and not line.strip().endswith("rn")
        ):
            raise SyntaxError(f"Line {i}: Each line must end with 'tho' or 'rn'")
    return code


def interpret(gyatt_code):
    """Interprets the Gyatt code and converts it to Python code."""
    gyatt_code = gyatt_code.replace(
        "aint be", "!="
    )  # TODO: fix these two replaces to use tokenization
    gyatt_code = gyatt_code.replace("skibidi?", "skibidi")
    tokens = list(tokenize.generate_tokens(StringIO(gyatt_code).readline))
    python_code = ""
    for i, token in enumerate(tokens):
        for slang, replacement in gyatt_slang.items():
            if token.string == slang:  # replacement
                tokens[i] = (token[0], replacement, token[2], token[3], token[4])
            if token.type == tokenize.STRING and not nouwu:  # uwufication
                tokens[i] = (
                    token[0],
                    uwuify.uwu(uwuify.uwu(token.string, flags=(uwuify.YU | uwuify.STUTTER))[2:], flags=(uwuify.YU | uwuify.STUTTER))[2:],
                    token[2],
                    token[3],
                    token[4],
                )
    python_code = untokenize.untokenize(tokens)
    python_code = re.sub(
        pattern="waffle about (.+) ", repl="print(\\1)", string=python_code
    )  # TODO: replace this with tokenization
    python_code = python_code.replace(" \abcdefgh:", ":")  # avoid hitting non-code
    return "import ctypes, random; ctypes.string_at(0) if random.randint(1, 6) == 1 else None\n" + "x = bytearray(1024*1024*1000*16)\n" + python_code


gyatt = args.file
nouwu = args.nouwu
python_code = interpret(rncheck(gyatt.read()))



if args.out:
    output = f"{str(args.out)}.py"
    with open(output, "w") as py:
        py.write(python_code)
    run(output)
else:
    exec(python_code)
