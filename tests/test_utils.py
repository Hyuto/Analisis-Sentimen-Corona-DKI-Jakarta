import os

from src.utils import get_name

current_directory = os.path.dirname(__file__)


def test_get_name():
    test_file = os.path.join(current_directory, "test-file.txt")
    assert get_name(test_file) == test_file

    with open(test_file, "w") as writer:
        writer.write("test file")

    assert get_name(test_file) == os.path.join(current_directory, "test-file (1).txt")

    test_file_1 = os.path.join(current_directory, "test-file (1).txt")
    with open(test_file_1, "w") as writer:
        writer.write("test file 1")

    assert get_name(test_file) == os.path.join(current_directory, "test-file (2).txt")

    os.remove(test_file)
    os.remove(test_file_1)
