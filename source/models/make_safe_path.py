replace_map = {
    '&': 'and',
    ' ': '_',
    '?': '',
    '*': '',
    '|': '',
    '<': '',
    '>': '',
    '"': '',
    ':': '',
    '/': '-',
    '\\': '-'
}

trans_table = str.maketrans(replace_map)

def make_safe_path(path: str) -> str:
    return path.translate(trans_table)
