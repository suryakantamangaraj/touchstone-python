import os
import pytest
from touchstone.parser import TouchstoneParser

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


def get_test_file(filename: str) -> str:
    return os.path.join(TEST_DATA_DIR, filename)


def test_parse_simple_s1p():
    filepath = get_test_file("simple.s1p")
    data = TouchstoneParser.parse(filepath)
    assert data.n_ports == 1
    assert data.n_freq > 0
    assert data.frequency[0] == 1e8


def test_parse_minimal_s2p():
    filepath = get_test_file("minimal.s2p")
    data = TouchstoneParser.parse(filepath)
    assert data.n_ports == 2
    assert data.n_freq > 0


def test_parse_comments_only_s2p():
    filepath = get_test_file("comments_only.s2p")
    data = TouchstoneParser.parse(filepath)
    assert data.n_ports == 2
    assert data.n_freq >= 0
    assert len(data.comments) > 0
