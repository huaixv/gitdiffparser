import sys

from lexer import lex
from parser import parse

if __name__ == "__main__":
    lines = sys.stdin.read().split('\n')
    lines = filter(None, lines)

    lexed = list(lex(lines))

    gitdiff = parse(lexed)
    for x in gitdiff.file_diffs:
        print(x)
