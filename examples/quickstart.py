import numpy as np
from touchstone.parser import read_snp


def create_dummy_s2p(filename):
    """Create a dummy .s2p file for demonstration."""
    content = """! Dummy S2P file
# GHZ S MA R 50
1.0  0.9 -10  0.1 80  0.1 80  0.9 -10
2.0  0.8 -20  0.2 70  0.2 70  0.8 -20
"""
    with open(filename, "w") as f:
        f.write(content)


def main():
    filename = "example.s2p"
    create_dummy_s2p(filename)

    print(f"Reading {filename}...")
    data = read_snp(filename)

    print(f"Number of ports: {data.n_ports}")
    print(f"Frequencies (Hz): {data.frequency}")

    # Access S21 magnitude in dB
    s21_db = data.magnitude(2, 1, db=True)
    print(f"S21 Magnitude (dB): {s21_db}")

    # Access S11 phase in degrees
    s11_phase = data.phase(1, 1, deg=True)
    print(f"S11 Phase (deg): {s11_phase}")

    # Get the raw S-parameter matrix at the first frequency point
    s_matrix_1ghz = data.s_parameters[0]
    print(f"S-matrix at {data.frequency[0]/1e9} GHz:\n{s_matrix_1ghz}")

    # Plotting example (requires matplotlib)
    try:
        import matplotlib.pyplot as plt

        print("\nGenerating S21 Magnitude plot...")
        plt.figure(figsize=(10, 6))
        plt.plot(data.frequency / 1e9, data.magnitude(2, 1), label="S21 (dB)")
        plt.title("S-Parameter Analysis")
        plt.xlabel("Frequency (GHz)")
        plt.ylabel("Magnitude (dB)")
        plt.grid(True)
        plt.legend()
        plt.savefig("s_parameter_plot.png")
        print("Plot saved to s_parameter_plot.png")
    except ImportError:
        print("\nMatplotlib not installed. Skipping plot generation.")


if __name__ == "__main__":
    main()
