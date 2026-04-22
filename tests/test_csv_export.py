import numpy as np

from touchstone.parser import TouchstoneData


def test_csv_export():
    freqs = np.array([1e9, 2e9])
    s = np.zeros((2, 2, 2), dtype=complex)
    s[0, 0, 0] = complex(0.5, 0.5)  # S11 mag ~0.707
    s[0, 1, 0] = complex(1.0, 0.0)  # S21 mag 1.0

    data = TouchstoneData(frequency=freqs, s_parameters=s)
    csv_str = data.to_csv_string()

    lines = csv_str.strip().split("\r\n" if "\r\n" in csv_str else "\n")
    assert len(lines) == 3
    assert "Frequency (Hz)" in lines[0]
    assert "S11_Mag" in lines[0]
    assert "S21_Mag" in lines[0]

    # Check first data row
    assert lines[1].startswith("1000000000.0")
