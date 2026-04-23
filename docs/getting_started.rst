Getting Started
===============

Installation
------------

Install **touchstone.parser** from PyPI:

.. code-block:: bash

   pip install touchstone.parser

To install with development dependencies:

.. code-block:: bash

   pip install "touchstone.parser[dev]"

For optional visualization support (matplotlib):

.. code-block:: bash

   pip install "touchstone.parser[viz]"

Requirements
------------

- Python 3.10 or higher
- NumPy ≥ 1.20.0

Quick Start
-----------

Parse a Touchstone file and inspect the data:

.. code-block:: python

   from touchstone.parser import TouchstoneParser

   # Parse a 2-port Touchstone file
   data = TouchstoneParser.parse("filter.s2p")

   print(f"Ports: {data.n_ports}")
   print(f"Frequency points: {data.n_freq}")

   # Query S21 insertion loss
   il = data.to_insertion_loss()
   for f, val in zip(data.frequencies, il):
       freq_ghz = f / 1e9
       print(f"{freq_ghz:.3f} GHz → IL = {val:.2f} dB")

Parse from a string instead of a file:

.. code-block:: python

   from touchstone.parser import TouchstoneParser

   content = (
       "! Example 1-port data\n"
       "# GHz S MA R 50\n"
       "1.0  0.9  -10.0\n"
       "2.0  0.8  -20.0\n"
   )

   data = TouchstoneParser.parse_string(content, n_ports=1)
   print(data)
