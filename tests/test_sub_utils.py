import os

import pytest

from narrator.sub_utils import make_filename, rand_str, crop_suffix, add_suffix


def test_rand_str():
    import random

    random.seed(1114111)
    assert rand_str(0) == ""
    assert rand_str(1) == "4"
    assert rand_str() == "2B22B142"
    assert rand_str(32) == "625F74C5BE0ED3794BA8376DDA6BD76B"


@pytest.mark.parametrize(
    "file_path",
    [
        "abcd",
        "abcd.efg",
        ".efg",
        os.path.join("ab", "cd", "efg"),
        os.path.join("ab", "cdef.g"),
    ],
)
def test_suffix(file_path):
    assert file_path == crop_suffix(file_path)
    assert file_path != add_suffix(file_path)
    assert add_suffix(file_path) != add_suffix(file_path)
    assert crop_suffix(add_suffix(file_path)) == crop_suffix(add_suffix(file_path))


def test_make_filename():
    for in_str in ["abc_def", "", "ы", "_-_aAфФ", "8053", " _-&%@#!()"]:
        assert make_filename(in_str) == in_str

    for in_str, out_str in [("-a!sd?gh*j$", "-a!sdghj"), ("`~№;^:?*<>", "")]:
        assert make_filename(in_str) == out_str
