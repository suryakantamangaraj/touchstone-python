import re
from typing import Iterable, Iterator


class DataLineTokenizer:
    def __init__(self):
        pass

    @staticmethod
    def get_numbers(lines: Iterable[str]) -> Iterator[float]:
        """Yield all numbers found in the lines, ignoring comments."""
        for line in lines:
            clean_line = line.split("!")[0].strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            parts = re.split(r"[\s,]+", clean_line)
            for part in parts:
                if part:
                    try:
                        yield float(part)
                    except ValueError:
                        continue
