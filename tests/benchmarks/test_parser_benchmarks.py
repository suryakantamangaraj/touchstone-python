from touchstone.parser import TouchstoneParser


def test_benchmark_parser(benchmark):
    # Generate a string representing a 10,000 point 2-port Touchstone file
    lines = ["# GHZ S MA R 50"]
    for i in range(10000):
        # frequency s11 s21 s12 s22
        lines.append(f"{1.0 + i * 0.001} 0.5 0 0.5 0 0.5 0 0.5 0")

    content = "\n".join(lines)

    def run_parser():
        return TouchstoneParser.parse_string(content, n_ports=2)

    result = benchmark(run_parser)

    assert result.n_freq == 10000
    assert result.n_ports == 2
