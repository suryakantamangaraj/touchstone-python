"""
Custom exceptions for the Touchstone parser.

This module defines :class:`TouchstoneParserException`, raised when the
parser encounters invalid or unexpected content in a Touchstone file.
"""

from typing import Optional


class TouchstoneParserException(Exception):
    """Exception raised for errors during Touchstone file parsing.

    When a line number is provided, it is appended to the error message
    for easier debugging.

    Attributes:
        line_number: The 1-based line number where the error occurred,
            or ``None`` if not applicable.

    Args:
        message: A human-readable description of the error.
        line_number: Optional 1-based line number where the error occurred.

    Example:
        >>> raise TouchstoneParserException("Invalid value", line_number=42)
        TouchstoneParserException: Invalid value (Line 42)
    """

    def __init__(self, message: str, line_number: Optional[int] = None):
        self.line_number = line_number

        if line_number is not None:
            message = f"{message} (Line {line_number})"
        super().__init__(message)
