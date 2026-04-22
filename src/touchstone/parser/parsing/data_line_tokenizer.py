"""
Tokenizer for parsing numerical data from Touchstone files.
"""

import re
from typing import Iterable, Iterator

from .touchstone_parser_exception import TouchstoneParserException


class DataLineTokenizer:
    """
    Utility class for tokenizing numerical data from lines.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_numbers(lines: Iterable[str]) -> Iterator[float]:
        """
        Yield all numbers found in the lines, ignoring comments.

        Args:
            lines (Iterable[str]): A sequence of string lines.

        Yields:
            float: The parsed numerical values.

        Raises:
            TouchstoneParserException: If a numeric value cannot be parsed.
        """
        for line_idx, line in enumerate(lines, start=1):
            clean_line = line.split("!")[0].strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            parts = re.split(r"[\s,]+", clean_line)
            for part in parts:
                if part:
                    try:
                        yield float(part)
                    except ValueError:
                        raise TouchstoneParserException(f"Invalid numeric value: '{part}'", line_idx)
