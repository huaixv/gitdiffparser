import sys

from lexer import lex
from parser import parse
from formatter import format

from astnodes import *

import re

# Keep only diffs which include lines with trailing spaces
def prune_diff(diff):
    if isinstance(diff, LineDiff):
        keep = re.search(r'^\+.*\s$', diff.line)
        return diff if keep else None
    elif isinstance(diff, NoNewline):
        return None
    elif isinstance(diff, ChunkDiff):
        line_diffs = list(map(prune_diff, diff.line_diffs))
        keep = any(filter(None, line_diffs))
        return diff if keep else None
    elif isinstance(diff, EmptyDiffContent):
        return None
    elif isinstance(diff, BinaryDiffContent):
        return None
    elif isinstance(diff, TextDiffContent):
        chunks = map(prune_diff, diff.chunks)
        chunks = list(filter(None, chunks))
        keep = len(chunks) > 0
        diff.chunks = chunks
        return diff if keep else None
    elif isinstance(diff, FileDiff):
        diff_content = prune_diff(diff.diff_content)
        keep = bool(diff_content)
        diff.diff_content = diff_content
        return diff if keep else None
    elif isinstance(diff, GitDiff):
        file_diffs = map(prune_diff, diff.file_diffs)
        file_diffs = list(filter(None, file_diffs))
        keep = len(file_diffs) > 0
        diff.file_diffs = file_diffs
        return diff if keep else None
    else:
        assert 0


if __name__ == "__main__":
    lines = sys.stdin.read().split('\n')
    lines = filter(None, lines)

    lexed = list(lex(lines))

    gitdiff = parse(lexed)
    gitdiff = prune_diff(gitdiff)

    newlines = format(gitdiff)
