import re

# Regular expressions
FILE_DIFF_HEADER = re.compile(r"^diff --git a/(?P<from_file>.*?)\s* b/(?P<to_file>.*?)\s*$")
SIM_INDEX_HEADER = re.compile(r"^similarity index (?P<sim>\d+%)$")
RENAME_FROM_HEADER = re.compile(r"^rename from (?P<from_file>.*)$")
RENAME_TO_HEADER = re.compile(r"^rename to (?P<to_file>.*)$")
OLD_MODE_HEADER = re.compile(r"^old mode (?P<mode>\d+)$")
NEW_MODE_HEADER = re.compile(r"^new mode (?P<mode>\d+)$")
NEW_FILE_MODE_HEADER = re.compile(r"^new file mode (?P<mode>\d+)$")
DELETED_FILE_MODE_HEADER = re.compile(r"^deleted file mode (?P<mode>\d+)$")
INDEX_DIFF_HEADER = re.compile(r"^index (?P<from_blob>.*?)\.\.(?P<to_blob>.*?)(?: (?P<mode>\d+))?$")
BINARY_DIFF = re.compile(r"Binary files (?P<from_file>.*) and (?P<to_file>.*) differ$")
A_FILE_CHANGE_HEADER = re.compile(r"^--- (?:/dev/null|a/(?P<file>.*?)\s*)$")
B_FILE_CHANGE_HEADER = re.compile(r"^\+\+\+ (?:/dev/null|b/(?P<file>.*?)\s*)$")
CHUNK_HEADER = re.compile(r"^@@ -(?P<from_line_start>\d+)(?:,(?P<from_line_count>\d+))? \+(?P<to_line_start>\d+)(?:,(?P<to_line_count>\d+))? @@(?P<line>.*)$")
LINE_DIFF = re.compile(r"^(?P<action>[-+ ])(?P<line>.*)$")
NO_NEWLINE = re.compile(r"^\\ No newline at end of file$")

REGEXS = [
    (FILE_DIFF_HEADER, "file_diff_header"),
    (SIM_INDEX_HEADER, "sim_index_header"),
    (RENAME_FROM_HEADER, "rename_from_header"),
    (RENAME_TO_HEADER, "rename_to_header"),
    (OLD_MODE_HEADER, "old_mode_header"),
    (NEW_MODE_HEADER, "new_mode_header"),
    (NEW_FILE_MODE_HEADER, "new_file_mode_header"),
    (DELETED_FILE_MODE_HEADER, "deleted_file_mode_header"),
    (INDEX_DIFF_HEADER, "index_diff_header"),
    (BINARY_DIFF, "binary_diff"),
    (A_FILE_CHANGE_HEADER, "a_file_change_header"),
    (B_FILE_CHANGE_HEADER, "b_file_change_header"),
    (CHUNK_HEADER, "chunk_header"),
    (LINE_DIFF, "line_diff"),
    (NO_NEWLINE, "no_newline"),
]

def lex(lines):
    for line in lines:
        for (regex, type_str) in REGEXS:
            match = regex.search(line)
            if match:
                yield type_str, line
                break
        else:
            print(line.encode())
            assert 0
