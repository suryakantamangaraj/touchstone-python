"""
Custom exceptions for the Touchstone parser.
"""

from typing import Optional


class TouchstoneParserException(Exception):
    """Exception raised for errors during Touchstone parsing."""

    def __init__(self, message: str, line_number: Optional[int] = None):
        self.line_number = line_number
        if line_number is not None:
            message = f"{message} (Line {line_number})"
        super().__init__(message)
