import time

import numpy as np
import pytest

from touchstone.parser import read_snp


def test_large_frequency_sweep(tmp_path):
    """Stress test with 100,000 frequency points."""
    d = tmp_path / "large.s1p"
    n_points = 100000

    # Generate data efficiently
    freqs = np.linspace(1, 100, n_points)
    data_lines = [f"{f} 0.5 0.5" for f in freqs]

    start_time = time.time()
    d.write_text("# GHZ S RI R 50\n" + "\n".join(data_lines))
    write_duration = time.time() - start_time
    print(f"Write duration: {write_duration:.2f}s")

    start_time = time.time()
    data = read_snp(str(d))
    parse_duration = time.time() - start_time

    print(f"Parsed {n_points} points in {parse_duration:.2f}s")
    assert len(data.frequency) == n_points
    # We target < 1 second for 100k points on modern hardware
    assert parse_duration < 5.0


def test_high_port_count(tmp_path):
    """Stress test with a 16-port file (s16p)."""
    n_ports = 16
    d = tmp_path / f"test.s{n_ports}p"

    # 16 ports means 16*16 = 256 complex parameters. 256 * 2 = 512 numbers + 1 freq = 513 numbers per line.
    n_params = n_ports**2
    nums_per_line = 1 + n_params * 2

    # Create one row of data
    row_data = [1.0] + [0.1] * (n_params * 2)
    row_str = " ".join(map(str, row_data))

    d.write_text(f"# GHZ S RI R 50\n{row_str}")

    start_time = time.time()
    data = read_snp(str(d))
    parse_duration = time.time() - start_time

    print(f"Parsed s{n_ports}p in {parse_duration:.4f}s")
    assert data.n_ports == n_ports
    assert data.s_parameters.shape == (1, 16, 16)
    assert data.s_parameters[0, 15, 15] == complex(0.1, 0.1)


def test_memory_usage_large_file(tmp_path):
    """Verify we don't crash on very large files (approx 100MB)."""
    d = tmp_path / "huge.s2p"
    n_points = 500000
    with open(d, "w") as f:
        f.write("# GHZ S RI R 50\n")
        for i in range(n_points):
            f.write(f"{i} 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1\n")

    start_time = time.time()
    data = read_snp(str(d))
    parse_duration = time.time() - start_time

    print(f"Parsed huge s2p (500k points) in {parse_duration:.2f}s")
    assert len(data.frequency) == n_points


def test_parsing_benchmark(tmp_path, benchmark):
    """Industry Standard: Benchmark parsing speed."""
    d = tmp_path / "benchmark.s2p"
    n_points = 10000
    with open(d, "w") as f:
        f.write("# GHZ S RI R 50\n")
        for i in range(n_points):
            f.write(f"{i} 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1\n")

    benchmark(read_snp, str(d))
