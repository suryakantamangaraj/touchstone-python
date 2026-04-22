"""
Core Touchstone file parser.
"""

import os
import re
from typing import List, Optional

import numpy as np

from ..models.data_format import DataFormat
from ..models.touchstone_data import TouchstoneData
from ..utilities.frequency_converter import normalize_frequency
from ..utilities.network_parameter_extensions import (
    db_to_complex,
    ma_to_complex,
    ri_to_complex,
)
from .data_line_tokenizer import DataLineTokenizer
from .option_line_parser import OptionLineParser
from .touchstone_parser_exception import TouchstoneParserException


class TouchstoneParser:
    """Parser for reading Touchstone (.sNp) files into structured data."""

    @staticmethod
    def _infer_n_ports(total_numbers: int) -> int:
        for n in range(1, 9):
            nums_per_freq = 1 + (n**2 * 2)
            if total_numbers > 0 and total_numbers % nums_per_freq == 0:
                return n
        return 2

    @staticmethod
    def _parse_lines(
        lines: List[str], n_ports: int = 0, filename: Optional[str] = None
    ) -> TouchstoneData:
        comments: List[str] = []
        options = None

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith("!"):
                comments.append(trimmed[1:].strip())
                continue

            clean_line = line.split("!")[0].strip()
            if clean_line.startswith("#"):
                options = OptionLineParser.parse(clean_line)
                break

        if options is None:
            options = OptionLineParser.parse("# GHZ S MA R 50")

        numbers = list(DataLineTokenizer.get_numbers(lines))

        if n_ports <= 0:
            n_ports = TouchstoneParser._infer_n_ports(len(numbers))

        nums_per_freq = 1 + (n_ports**2 * 2)
        if len(numbers) % nums_per_freq != 0:
            n_points = len(numbers) // nums_per_freq
            numbers = numbers[: n_points * nums_per_freq]
        else:
            n_points = len(numbers) // nums_per_freq

        if len(numbers) == 0:
            # Handle empty data
            return TouchstoneData(
                frequency=np.array([]),
                s_parameters=np.zeros((0, n_ports, n_ports), dtype=complex),
                options=options,
                comments=comments,
                filename=filename,
            )

        data = np.array(numbers).reshape(n_points, nums_per_freq)

        freqs = np.array(
            [normalize_frequency(f, options.frequency_unit.value) for f in data[:, 0]]
        )
        raw_s = data[:, 1:]

        s_params = np.zeros((n_points, n_ports, n_ports), dtype=complex)

        def to_complex(v1, v2):
            if options.data_format == DataFormat.RI:
                return ri_to_complex(v1, v2)
            elif options.data_format == DataFormat.DB:
                return db_to_complex(v1, v2)
            else:
                return ma_to_complex(v1, v2)

        for p in range(n_points):
            row = raw_s[p]
            if n_ports == 1:
                s_params[p, 0, 0] = to_complex(row[0], row[1])
            elif n_ports == 2:
                s_params[p, 0, 0] = to_complex(row[0], row[1])
                s_params[p, 1, 0] = to_complex(row[2], row[3])
                s_params[p, 0, 1] = to_complex(row[4], row[5])
                s_params[p, 1, 1] = to_complex(row[6], row[7])
            else:
                idx = 0
                for i in range(n_ports):
                    for j in range(n_ports):
                        s_params[p, i, j] = to_complex(row[idx], row[idx + 1])
                        idx += 2

        return TouchstoneData(
            frequency=freqs,
            s_parameters=s_params,
            options=options,
            comments=comments,
            filename=filename,
        )

    @staticmethod
    def parse(filepath: str) -> TouchstoneData:
        """
        Parse a Touchstone file from disk.

        Args:
            filepath (str): Path to the .sNp file.

        Returns:
            TouchstoneData: The parsed data.

        Raises:
            TouchstoneParserException: If the file extension is invalid.
        """
        filename = os.path.basename(filepath)
        ext_match = re.search(r"\.s(\d+)p$", filename.lower())
        if not ext_match:
            raise TouchstoneParserException(
                f"Could not determine port count from extension of {filepath}"
            )

        n_ports = int(ext_match.group(1))

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        return TouchstoneParser._parse_lines(lines, n_ports=n_ports, filename=filename)

    @staticmethod
    def parse_string(
        content: str, n_ports: int = 0, filename: Optional[str] = None
    ) -> TouchstoneData:
        """
        Parse Touchstone data from a string.

        Args:
            content (str): The raw Touchstone file content.
            n_ports (int): Number of ports. 0 to auto-detect.
            filename (Optional[str]): Optional filename for metadata.

        Returns:
            TouchstoneData: The parsed data.
        """
        lines = content.splitlines()
        return TouchstoneParser._parse_lines(lines, n_ports=n_ports, filename=filename)
