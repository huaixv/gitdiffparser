from astnodes import *

def format(diff):
    if isinstance(diff, FileDiffHeader):
        return diff.header
    elif isinstance(diff, DiffHeader):
        return diff.index_diff_header
    elif isinstance(diff, ChangeDiffType):
        return format(diff.diff_header)
    elif isinstance(diff, NewDiffType):
        return '\n'.join([diff.new_file_mode, format(diff.diff_header)])
    elif isinstance(diff, DeleteDiffType):
        return '\n'.join([diff.deleted_file_mode, format(diff.diff_header)])
    elif isinstance(diff, RenameDiffType):
        return '\n'.join([diff.sim_index, diff.rename_from, diff.rename_to])
    elif isinstance(diff, EmptyDiffContent):
        return None
    elif isinstance(diff, BinaryDiffContent):
        return diff.binary_diff
    elif isinstance(diff, LineDiff):
        return diff.line
    elif isinstance(diff, NoNewline):
        return diff.line
    elif isinstance(diff, ChunkDiff):
        return "\n".join([diff.chunk_header] + list(map(format, diff.line_diffs)))
    elif isinstance(diff, TextDiffContent):
        return "\n".join(
            [diff.a_file_change_header, diff.b_file_change_header]
            + list(map(format, diff.chunks))
        )
    elif isinstance(diff, FileDiff):
        return "\n".join(filter(None, map(format, [diff.header, diff.diff_type, diff.diff_content])))
    elif isinstance(diff, GitDiff):
        return '\n'.join(map(format, diff.file_diffs))
    else:
        assert 0
