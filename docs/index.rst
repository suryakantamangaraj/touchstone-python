touchstone.parser Documentation
================================

.. image:: https://img.shields.io/pypi/v/touchstone.parser?style=flat-square&logo=pypi&label=PyPI
   :target: https://pypi.org/project/touchstone.parser/
   :alt: PyPI Version

.. image:: https://img.shields.io/github/actions/workflow/status/suryakantamangaraj/touchstone-python/ci.yml?branch=main&style=flat-square&logo=github&label=CI
   :target: https://github.com/suryakantamangaraj/touchstone-python/actions/workflows/ci.yml
   :alt: CI Status

.. image:: https://img.shields.io/github/license/suryakantamangaraj/touchstone-python?style=flat-square
   :target: https://github.com/suryakantamangaraj/touchstone-python/blob/main/LICENSE
   :alt: License

**touchstone.parser** is a clean, modular, enterprise-ready Python library for
parsing `Touchstone <https://ibis.org/>`_ (``.sNp``) files — the industry-standard
format for RF and microwave S-parameter data.

It provides strongly typed classes, query-friendly APIs, and seamless integration
into simulation and analysis workflows.

Key Features
------------

- **Parse ``.sNp`` files** into strongly typed Python classes
- **Multi-port support** — 1-port through N-port networks
- **All data formats** — Real/Imaginary (RI), Magnitude/Angle (MA), Decibel/Angle (DB)
- **All frequency units** — Hz, kHz, MHz, GHz with automatic normalization
- **All parameter types** — S, Y, Z, H, G
- **RF calculations** — insertion loss, return loss, VSWR out of the box
- **Export utilities** — CSV export and Touchstone writer for round-trip fidelity
- **Minimal dependencies** — powered by ``numpy`` for fast array operations

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started
   usage
   api
