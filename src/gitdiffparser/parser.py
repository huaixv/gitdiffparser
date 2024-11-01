import os
import sys

from astnodes import *

def parse(lexed):
    def check(type_str):
        nonlocal lexed

        if lexed:
            head = lexed[0]
            return head[0] == type_str
        else:
            return False

    def consume(type_str):
        nonlocal lexed
        assert check(type_str)

        head, *lexed = lexed
        return head[1]

    def parser_gitdiff():
        file_diffs = []
        while lexed:
            file_diffs.append(parser_filediff())
        return GitDiff(
            file_diffs=file_diffs
        )

    def parser_filediff():
        header = parser_file_header()
        diff_type = parser_difftype()
        if isinstance(diff_type, RenameDiffType):
            return FileDiff(
                header=header,
                diff_type=diff_type,
                diff_content=EmptyDiffContent()
            )
        else:
            return FileDiff(
                header=header,
                diff_type=diff_type,
                diff_content=parser_diffcontent()
            )

    def  parser_file_header():
        header = consume("file_diff_header")
        return FileDiffHeader(
            header=header
        )

    def parser_difftype():
        if check("index_diff_header"):
            return ChangeDiffType(
                diff_header=parser_diff_header()
            )
        if check("new_file_mode_header"):
            return NewDiffType(
                new_file_mode=consume("new_file_mode_header"),
                diff_header=parser_diff_header()
            )
        elif check("deleted_file_mode_header"):
            return DeleteDiffType(
                deleted_file_mode=consume("deleted_file_mode_header"),
                diff_header=parser_diff_header()
            )
        elif check("sim_index_header"):
            return RenameDiffType(
                sim_index=consume("sim_index_header"),
                rename_from=consume("rename_from_header"),
                rename_to=consume("rename_to_header")
            )
        else:
            assert 0

    def parser_diff_header():
        return DiffHeader(
            index_diff_header=consume("index_diff_header"),
        )

    def parser_line_diffs():
        line_diffs = []
        while check("line_diff") or check("no_newline"):
            if check("line_diff"):
                line_diff = LineDiff(
                    line=consume("line_diff")
                )
            elif check("no_newline"):
                line_diff = NoNewline(
                    line=consume("no_newline")
                )
            else:
                assert 0
            line_diffs.append(line_diff)
        return line_diffs

    def parser_chunk():
        chunk = ChunkDiff(
            chunk_header=consume("chunk_header"),
            line_diffs=parser_line_diffs()
        )
        return chunk

    def parser_diffcontent():
        if check("binary_diff"):
            return BinaryDiffContent(
                binary_diff=consume("binary_diff")
            )
        elif check("a_file_change_header"):
            a_file_change_header=consume("a_file_change_header")
            b_file_change_header=consume("b_file_change_header")
            chunks = []
            while check("chunk_header"):
                chunks.append(parser_chunk())
            return TextDiffContent(
                a_file_change_header=a_file_change_header,
                b_file_change_header=b_file_change_header,
                chunks=chunks
            )
        elif check("file_diff_header"):
            return EmptyDiffContent()
        else:
            assert 0

    return parser_gitdiff()
