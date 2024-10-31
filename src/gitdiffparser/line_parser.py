SIM_INDEX_HEADER = re.compile(r"^similarity index (?P<sim>\d+%)$")
RENAME_FROM_HEADER = re.compile(r"^rename from (?P<from_file>.*)$")
RENAME_TO_HEADER = re.compile(r"^rename to (?P<to_file>.*)$")
    if prev_state in ("start_of_file", "rename_to_header", "new_mode_header", "line_diff", "no_newline", "index_diff_header", "binary_diff"):
    # "similarity index {SIM}"
    if prev_state == "file_diff_header":
        match = SIM_INDEX_HEADER.search(line)
        if match:
            return "sim_index_header", match.groupdict()
    
    # "rename from {FROM_FILE}"
    if prev_state == "sim_index_header":
        match = RENAME_FROM_HEADER.search(line)
        if match:
            return "rename_from_header", match.groupdict()
    
    # "rename to {TO_FILE}"
    if prev_state == "rename_from_header":
        match = RENAME_TO_HEADER.search(line)
        if match:
            return "rename_to_header", match.groupdict()
