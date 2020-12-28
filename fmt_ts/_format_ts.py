#!/usr/bin/python3
import re
import subprocess
import argparse
import os

def main():
    parser = argparse.ArgumentParser("fmt-ts")
    parser.add_argument("file", type=str, help="input file")
    parser.add_argument("-r", action="store_true", help="replace input file")
    args = parser.parse_args()

    # First format it using tsfmt. tsfmt.json specifies function bracket start
    # on new line.

    try:
        textlines = subprocess.check_output([
            "tsfmt",
            args.file,
            "--baseDir",
            os.path.dirname(os.path.abspath(__file__)),
        ], encoding="utf-8", universal_newlines=True, stderr=subprocess.STDOUT).splitlines()
    except subprocess.CalledProcessError as exc:
        print(exc.output, end="")
        exit(1)

    # Matches named function declarations so "function foo()"
    # but not "function ()" and not "function()"
    pattern = re.compile(r"(function(?! (\()|(\()))")

    # Matches all white space at start of line
    whitespace = re.compile(r"^(\s*)")

    # Then place function def on a new line.
    for i, text in enumerate(textlines):
        matches = [m.start() for m in pattern.finditer(text)]
        indent_match = whitespace.match(text)
        assert len(indent_match.groups()) == 1
        indent = indent_match.groups()[0]
        if matches:
            line = text[matches[0]:].replace("function ", "function\n" + indent)
            textlines[i] = text[:matches[0]] + line

        if (pos := text.find("function* ")) != -1:
            line = text[pos:].replace("function* ", "function *\n" + indent)
            textlines[i] = text[:pos] + line

    if args.r:
        with open(args.file, "w") as fp:
            fp.write("\n".join(textlines))
    else:
        print("\n".join(textlines))