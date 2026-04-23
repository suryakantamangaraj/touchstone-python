"""
touchstone namespace package.

This is the top-level namespace package for the ``touchstone`` distribution.
It uses ``pkgutil.extend_path`` to allow multiple distributions to contribute
sub-packages under the ``touchstone`` namespace.
"""

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
