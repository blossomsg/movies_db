"""Modules to fix spellings"""

import re
from typing import List


def fix_spellings(pattern: str, column_category: List[str], new_name: str) -> None:
    """
    This tool fixes the spelling mistakes from a list using index position,
    and updates the list with correct spelling.
    Args:
        pattern(str): A regular expression pattern
        column_category(List(str)): Column name in which you want to fix spelling
        new_name(str): Correct Spelling
    """
    compile_pattern = re.compile(f"({pattern})")
    get_idx = [
        column_category.index(value)
        for value in column_category
        if compile_pattern.search(value)
    ]
    for idx in get_idx:
        column_category[idx] = new_name
