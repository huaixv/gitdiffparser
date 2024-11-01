from dataclasses import dataclass, field
from typing import List, Optional, Union

# AST Node Definitions

# File diff header
@dataclass
class FileDiffHeader:
    header: str


# Diff types
@dataclass
class DiffType:
    pass

# Diff header
@dataclass
class DiffHeader:
    index_diff_header: str

# Diff Type
@dataclass
class ChangeDiffType(DiffType):
    diff_header: DiffHeader

@dataclass
class NewDiffType(DiffType):
    new_file_mode: str
    diff_header: DiffHeader

@dataclass
class DeleteDiffType(DiffType):
    deleted_file_mode: str
    diff_header: DiffHeader

@dataclass
class RenameDiffType(DiffType):
    sim_index: str
    rename_from: str
    rename_to: str

# Diff content
@dataclass
class DiffContent:
    pass

@dataclass
class EmptyDiffContent(DiffContent):
    pass

@dataclass
class BinaryDiffContent(DiffContent):
    binary_diff: str

@dataclass
class LineDiff:
    line: str

@dataclass
class NoNewline:
    line: str

@dataclass
class ChunkDiff:
    chunk_header: FileDiffHeader
    line_diffs: List[Union[LineDiff, NoNewline]] = field(default_factory=list)


@dataclass
class TextDiffContent:
    a_file_change_header: str
    b_file_change_header: str
    chunks: List[ChunkDiff]

# File Diff
@dataclass
class FileDiff:
    header: FileDiffHeader
    diff_type: DiffType
    diff_content: Union[EmptyDiffContent, BinaryDiffContent, TextDiffContent]


# Git Diff
@dataclass
class GitDiff:
    file_diffs: List[FileDiff] = field(default_factory=list)
