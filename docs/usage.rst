Usage Guide
===========

This page covers the main workflows and features of ``touchstone.parser``.

Parsing Files
-------------

Parse a Touchstone file from disk:

.. code-block:: python

   from touchstone.parser import TouchstoneParser

   data = TouchstoneParser.parse("amplifier.s2p")

The parser auto-detects the number of ports from the file extension (``.s1p``,
``.s2p``, ``.s3p``, etc.) and parses the option line, comments, and data.

Accessing S-Parameters
----------------------

Access individual S-parameters across all frequencies:

.. code-block:: python

   # Get S21 (transmission) as a complex array
   s21 = data.get_s(to_port=2, from_port=1)

   # Get S11 (reflection) as a complex array
   s11 = data.get_s(to_port=1, from_port=1)

Access data at a specific frequency index:

.. code-block:: python

   # Get the FrequencyPoint at index 0
   point = data[0]
   print(point.frequency_hz)

   # Access a specific parameter from the matrix
   s11_at_point = point[0, 0]
   print(s11_at_point.magnitude_db)

RF Calculations
---------------

Compute common RF metrics directly from the parsed data:

.. code-block:: python

   # Insertion loss (|S21| in dB, positive values)
   il = data.to_insertion_loss()

   # Return loss (|S11| in dB, positive values)
   rl = data.to_return_loss()

   # Voltage Standing Wave Ratio from S11
   vswr = data.to_vswr()

Filtering Data
--------------

Filter data to a specific frequency range:

.. code-block:: python

   # Keep only data in the 2–3 GHz range
   passband = data.in_frequency_range(2.0e9, 3.0e9)
   print(f"Filtered points: {passband.n_freq}")

Use a custom predicate for advanced filtering:

.. code-block:: python

   # Keep only frequencies where S11 magnitude < 0.5
   import numpy as np

   filtered = data.where(lambda pt: np.abs(pt[0, 0].value) < 0.5)

Exporting Data
--------------

Export parsed data to CSV:

.. code-block:: python

   # Write to a CSV file
   data.to_csv("output.csv")

   # Or get the CSV as a string
   csv_string = data.to_csv_string()

Write back to Touchstone format (round-trip):

.. code-block:: python

   from touchstone.parser import write_snp

   write_snp(data, "output.s2p")

Conversion Utilities
--------------------

Use standalone conversion functions:

.. code-block:: python

   from touchstone.parser import (
       db_to_mag, mag_to_db,
       deg_to_rad, rad_to_deg,
       ma_to_complex, db_to_complex, ri_to_complex,
       normalize_frequency,
   )

   # Convert -3 dB to linear magnitude
   mag = db_to_mag(-3)  # ≈ 0.7079

   # Normalize 2.4 GHz to Hz
   freq_hz = normalize_frequency(2.4, "GHz")  # 2.4e9

Working with NetworkParameter
-----------------------------

The :class:`~touchstone.parser.models.network_parameter.NetworkParameter` class
provides rich access to individual S-parameter values:

.. code-block:: python

   from touchstone.parser.models.network_parameter import NetworkParameter

   # Create from magnitude and angle
   param = NetworkParameter.from_magnitude_angle(0.9, -45.0)

   print(param.magnitude)       # 0.9
   print(param.magnitude_db)    # ≈ -0.92 dB
   print(param.phase_degrees)   # -45.0
   print(param.real)            # real component
   print(param.imaginary)       # imaginary component

   # Arithmetic operations
   result = param * 2.0
   conjugate = param.conjugate()

Supported Formats
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 10

   * - Feature
     - Supported
   * - Touchstone v1.0 / v1.1
     - ✅
   * - 1-port (``.s1p``)
     - ✅
   * - 2-port (``.s2p``)
     - ✅
   * - Multi-port (``.s3p``, ``.s4p``, …)
     - ✅
   * - Real-Imaginary (RI)
     - ✅
   * - Magnitude-Angle (MA)
     - ✅
   * - Decibel-Angle (DB)
     - ✅
   * - Hz / kHz / MHz / GHz
     - ✅
   * - S / Y / Z / H / G parameters
     - ✅
   * - Comments and metadata
     - ✅
