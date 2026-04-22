"""
Comprehensive example showing parser capabilities, extensions, and models.
"""
import asyncio
import io
import numpy as np

from touchstone.parser import TouchstoneParser
from touchstone.parser.utilities.touchstone_data_extensions import get_s21


def create_dummy_s2p():
    content = """! Comprehensive S2P Demo
# MHZ S MA R 50
100  0.9 -10  0.1 80  0.1 80  0.9 -10
200  0.8 -20  0.5 70  0.5 70  0.8 -20
300  0.7 -30  0.8 60  0.8 60  0.7 -30
"""
    return io.StringIO(content)


async def main():
    stream = create_dummy_s2p()
    print("Parsing from stream...")
    data = TouchstoneParser.parse_stream(stream, filename="demo.s2p")

    print(f"\nParsed {data.count} points with {data.n_ports} ports.")
    print(f"Options: {data.options}")

    # Use LINQ-like where filter
    print("\nFiltering frequencies >= 200 MHz:")
    filtered = data.where(lambda p: p.frequency_hz >= 200e6)
    print(f"Filtered points: {filtered.count}")

    # Point-by-point access via indexer
    print("\nPoint-by-Point Access:")
    for i in range(data.count):
        pt = data[i]
        s11 = pt[0, 0]  # NetworkParameter
        s21 = pt[1, 0]
        print(f"  {pt.frequency_hz / 1e6:3.0f} MHz: S11={s11.magnitude:.2f}, S21={s21.magnitude:.2f}")

    # S-Parameter Tuples
    print("\nS21 Tuples:")
    for freq, param in get_s21(data):
        print(f"  {freq / 1e6:3.0f} MHz: {param.magnitude_db:.2f} dB")

    # CSV Export
    print("\nCSV Export (DB format):")
    from touchstone.parser.models.data_format import DataFormat
    csv_str = data.to_csv_string(format=DataFormat.DB)
    print(csv_str.strip())


if __name__ == "__main__":
    asyncio.run(main())
