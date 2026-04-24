"""
Touchstone.Parser — Plotting Example
Demonstrates how to visualize S-parameter data using matplotlib.

Mirrors the .NET Touchstone.Plotting.Example project.

Requirements:
    pip install matplotlib
    (or: pip install touchstone.parser[viz])
"""

import os
import sys

import numpy as np

# ════════════════════════════════════════════════════════════════════
#  Touchstone.Parser — Plotting Example
#  Demonstrates how to visualize S-parameter data using matplotlib
# ════════════════════════════════════════════════════════════════════


def main():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Error: matplotlib is required for this example.")
        print("Install it with: pip install matplotlib")
        print("  or: pip install touchstone.parser[viz]")
        sys.exit(1)

    from touchstone.parser import TouchstoneParser
    from touchstone.parser.utilities.touchstone_data_extensions import (
        get_magnitude,
        get_phase,
    )

    print("📊 Touchstone Plotting Demo")
    print("══════════════════════════")

    # 1. Parse the Touchstone file
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    file_path = os.path.join(sample_dir, "wifi_filter.s2p")
    data = TouchstoneParser.parse(file_path)

    print(f"Loaded {file_path} ({data.count} points)")

    # 2. Prepare data for plotting
    frequencies_ghz = data.frequency / 1e9
    s11_db = get_magnitude(data, 1, 1, db=True)
    s21_db = get_magnitude(data, 2, 1, db=True)

    # 3. Create S-parameter magnitude plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # S11 and S21 magnitude
    ax1.plot(frequencies_ghz, s11_db, "b-", linewidth=2, label="S11 (Return Loss)")
    ax1.plot(frequencies_ghz, s21_db, "r-", linewidth=2, label="S21 (Insertion Loss)")
    ax1.set_title("Filter S-Parameters", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Magnitude (dB)")
    ax1.set_ylim(-60, 5)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="best")
    ax1.axhline(y=-3, color="gray", linestyle="--", alpha=0.5, label="-3 dB line")

    # S11 and S21 phase
    s11_phase = get_phase(data, 1, 1, deg=True)
    s21_phase = get_phase(data, 2, 1, deg=True)

    ax2.plot(frequencies_ghz, s11_phase, "b-", linewidth=2, label="S11 Phase")
    ax2.plot(frequencies_ghz, s21_phase, "r-", linewidth=2, label="S21 Phase")
    ax2.set_xlabel("Frequency (GHz)")
    ax2.set_ylabel("Phase (degrees)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="best")

    plt.tight_layout()

    # 4. Save the plot
    output_path = os.path.join(os.path.dirname(__file__), "s_parameters_plot.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")

    print(f"✅ Plot saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
