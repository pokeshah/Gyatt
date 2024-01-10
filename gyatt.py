import re
import argparse
import tokenize
import io
import untokenize

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
}

def interpret(gyatt_code: str) -> str:
    assert type(gyatt_code) == str
    tokens = list(tokenize.generate_tokens(io.StringIO(gyatt_code).readline))
    python_code = ""
    for i, token in enumerate(tokens):
        for slang, replacement in gyatt_slang.items():
            if token.string == slang:
                tokens[i] = (token[0], replacement, token[2], token[3], token[4])
    python_code = untokenize.untokenize(tokens)
    python_code = re.sub(pattern="yap about (.+) rn", repl="print(\\1)", string=python_code)
    return python_code


if __name__ == "__main__":
    # Parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    parser.add_argument("-o", "--out", type=str, metavar="PATH", help="Compile and save the code into a Python script at PATH")
    args = parser.parse_args()
    # Interpret & execute the code
    with args.file as gyatt:
        python_code = interpret(gyatt.read())
        if args.out is not None:
            with open(args.out, "w") as py:
                py.truncate(0)
                py.write(python_code)
        else:
            exec(python_code)
