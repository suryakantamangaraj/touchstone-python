"""
Core Touchstone file parser.

This module contains the :class:`TouchstoneParser` class, which provides
static methods for reading Touchstone (``.sNp``) files from disk, strings,
or streams and converting them into :class:`~touchstone.parser.models.touchstone_data.TouchstoneData` objects.
"""

import os
import re
from typing import Iterable, List, Optional, TextIO

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
    """Parser for reading Touchstone (.sNp) files into structured data.

    All methods are static — there is no need to instantiate this class.

    Example:
        >>> data = TouchstoneParser.parse("filter.s2p")
        >>> data.n_ports
        2
    """

    @staticmethod
    def _infer_n_ports(total_numbers: int) -> int:
        """Infer the number of ports from the total count of numeric values.

        Each frequency point contributes ``1 + 2*N²`` numbers (one frequency
        value plus N² complex pairs). This method tries N from 1 to 8 and
        returns the first that evenly divides ``total_numbers``.

        Args:
            total_numbers: The total count of parsed numeric values.

        Returns:
            int: The inferred number of ports, defaulting to 2 if no
            match is found.
        """
        for n in range(1, 9):
            nums_per_freq = 1 + (n**2 * 2)
            if total_numbers > 0 and total_numbers % nums_per_freq == 0:
                return n
        return 2

    @staticmethod
    def _parse_lines(
        lines: Iterable[str], n_ports: int = 0, filename: Optional[str] = None
    ) -> TouchstoneData:
        """Parse Touchstone data from an iterable of text lines.

        This is the core parsing method used by all public entry points.
        It processes comments, the option line, and numerical data lines
        to produce a fully populated :class:`TouchstoneData` instance.

        Args:
            lines: An iterable of string lines (e.g., from a file or
                ``str.splitlines()``).
            n_ports: Number of ports. If ``0``, the port count is
                auto-detected from the data.
            filename: Optional filename for metadata.

        Returns:
            TouchstoneData: The parsed data.

        Raises:
            TouchstoneParserException: If multiple option lines are found
                or numeric values cannot be parsed.
        """
        comments: List[str] = []
        options = None

        lines_list = list(lines) if not isinstance(lines, list) else lines

        for line_idx, line in enumerate(lines_list, start=1):
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith("!"):
                # Only collect comments that appear before data or options?
                # The original just collected everything. We'll keep it.
                comments.append(trimmed[1:].strip())
                continue

            clean_line = line.split("!")[0].strip()
            if clean_line.startswith("#"):
                if options is not None:
                    raise TouchstoneParserException(
                        "Multiple option lines found", line_idx
                    )
                options = OptionLineParser.parse(clean_line)

        if options is None:
            options = OptionLineParser.parse("# GHZ S MA R 50")

        numbers = list(DataLineTokenizer.get_numbers(lines_list))

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
    def detect_port_count(filename: str) -> int:
        """Detect the number of ports from the filename extension.

        Parses the ``.sNp`` extension to extract the port count ``N``.

        Args:
            filename: The name of the file (e.g. ``'filter.s2p'``).

        Returns:
            int: The detected number of ports.

        Raises:
            TouchstoneParserException: If the extension does not match
                the ``.sNp`` pattern.
            ValueError: If the filename is null or empty.

        Example:
            >>> TouchstoneParser.detect_port_count("amp.s4p")
            4
        """
        if not filename:
            raise ValueError("filename cannot be null or empty")

        base = os.path.basename(filename)
        ext_match = re.search(r"\.s(\d+)p$", base.lower())
        if not ext_match:
            raise TouchstoneParserException(
                f"Could not determine port count from extension of {filename}"
            )
        return int(ext_match.group(1))

    @staticmethod
    def parse(filepath: str) -> TouchstoneData:
        """Parse a Touchstone file from disk.

        The port count is auto-detected from the file extension.

        Args:
            filepath: Absolute or relative path to the ``.sNp`` file.

        Returns:
            TouchstoneData: The fully parsed data.

        Raises:
            TouchstoneParserException: If the file extension is invalid.
            ValueError: If filepath is empty.
            FileNotFoundError: If the file does not exist.

        Example:
            >>> data = TouchstoneParser.parse("filter.s2p")
        """
        if not filepath:
            raise ValueError("filepath cannot be null or empty")

        filename = os.path.basename(filepath)
        n_ports = TouchstoneParser.detect_port_count(filename)

        with open(filepath, "r", encoding="utf-8") as f:
            return TouchstoneParser._parse_lines(f, n_ports=n_ports, filename=filename)

    @staticmethod
    def parse_string(
        content: str, n_ports: int = 0, filename: Optional[str] = None
    ) -> TouchstoneData:
        """Parse Touchstone data from a string.

        Args:
            content: The raw Touchstone file content as a string.
            n_ports: Number of ports. Pass ``0`` to auto-detect from the
                data (default).
            filename: Optional filename for metadata purposes.

        Returns:
            TouchstoneData: The parsed data.

        Example:
            >>> data = TouchstoneParser.parse_string(raw_text, n_ports=2)
        """
        lines = content.splitlines()
        return TouchstoneParser._parse_lines(lines, n_ports=n_ports, filename=filename)

    @staticmethod
    def parse_stream(stream: TextIO, filename: Optional[str] = None) -> TouchstoneData:
        """Parse Touchstone data from a text stream.

        If a filename is provided, the port count is detected from its
        extension. Otherwise, it is auto-detected from the data.

        Args:
            stream: A readable text stream (e.g., ``io.StringIO``).
            filename: Optional filename for port detection and metadata.

        Returns:
            TouchstoneData: The parsed data.

        Example:
            >>> import io
            >>> stream = io.StringIO(raw_text)
            >>> data = TouchstoneParser.parse_stream(stream, filename="test.s2p")
        """
        n_ports = 0
        if filename:
            try:
                n_ports = TouchstoneParser.detect_port_count(filename)
            except TouchstoneParserException:
                pass

        return TouchstoneParser._parse_lines(stream, n_ports=n_ports, filename=filename)

    @staticmethod
    async def parse_async(filepath: str) -> TouchstoneData:
        """Asynchronously parse a Touchstone file from disk.

        Delegates to :meth:`parse` in a background thread using
        :func:`asyncio.to_thread`.

        Args:
            filepath: Path to the ``.sNp`` file.

        Returns:
            TouchstoneData: The parsed data.

        Example:
            >>> data = await TouchstoneParser.parse_async("filter.s2p")
        """
        import asyncio

        return await asyncio.to_thread(TouchstoneParser.parse, filepath)
