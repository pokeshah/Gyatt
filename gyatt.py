import re
import argparse
import os
import tokenize
import io
import untokenize

if os.path.exists("compiled.py"):
    os.remove("compiled.py")


gyatt_slang = {
    "lrizz": "False",
    "norizz": "None",
    "wrizz": "True",
    "also": "and",
    "masquerade": "as",
    "skibidi": "assert",
    "stawp": "break",
    "next": "continue",
    "gyatt": "def",
    "imposter": "elif",
    "crewmate": "else",
    "oof": "except",
    "frfr": "finally",
    "yapfor": "for",
    "yoinked": "from",
    "sus": "if",
    "steal": "import",
    "infam": "in",
    "be": "==",
    "anon": "lambda",
    "nogatekeep": "nonlocal",
    "aint": "not",
    "idk": "or",
    "whatever": "pass",
    "fanumtax": "raise",
    "yeet": "return",
    "yolo": "try",
    "yapuntil": "while",
    "chill": "yield",
    "nerd": "math",
    "rando": "random",
    "numba": "randint",
    "startyapping": "input",
    "mid": "min",
    "peak": "max",
}

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType("r"))
args = parser.parse_args()


def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())


def interpret(gyatt_code):
    tokens = list(tokenize.generate_tokens(io.StringIO(gyatt_code).readline))
    python_code = ""
    for i, token in enumerate(tokens):
        for slang, replacement in gyatt_slang.items():
            if token.string == slang:
                tokens[i] = (token[0], replacement, token[2], token[3], token[4])
    python_code = untokenize.untokenize(tokens)
    python_code = re.sub(
        pattern="yap about (.+) rn", repl="print(\\1)", string=python_code
    )
    return python_code


with args.file as gyatt:
    python_code = interpret(gyatt.read())
    with open("compiled.py", "x") as py:
        py.write(python_code)

run("compiled.py")
