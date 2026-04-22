import pytest
from touchstone.parser import TouchstoneParser

def test_missing_file_throws():
    with pytest.raises(Exception):
        TouchstoneParser.parse("nonexistent_file.s1p")
