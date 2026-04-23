"""
Tokenizer for parsing numerical data from Touchstone files.

This module provides the :class:`DataLineTokenizer` class, which extracts
floating-point numbers from data lines while skipping comments and
option lines.
"""

import re
from typing import Iterable, Iterator

from .touchstone_parser_exception import TouchstoneParserException


class DataLineTokenizer:
    """Utility class for tokenizing numerical data from Touchstone file lines.

    Data lines in a Touchstone file contain whitespace- or comma-separated
    floating-point numbers. Comment lines (starting with ``!``) and option
    lines (starting with ``#``) are skipped.

    Example:
        >>> lines = ["# GHz S MA R 50", "1.0  0.9  -10.0"]
        >>> list(DataLineTokenizer.get_numbers(lines))
        [1.0, 0.9, -10.0]
    """

    def __init__(self):
        """Initialize the DataLineTokenizer (no-op)."""
        pass

    @staticmethod
    def get_numbers(lines: Iterable[str]) -> Iterator[float]:
        """Yield all numeric values found in the data lines.

        Processes each line by stripping inline comments (``!``),
        skipping option lines (``#``) and blank lines, and parsing
        the remaining whitespace/comma-separated tokens as floats.

        Args:
            lines: An iterable of string lines from a Touchstone file.

        Yields:
            float: Each parsed numerical value, in order of appearance.

        Raises:
            TouchstoneParserException: If a token cannot be parsed as a
                float, with the line number included in the message.
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
                        raise TouchstoneParserException(
                            f"Invalid numeric value: '{part}'", line_idx
                        )
