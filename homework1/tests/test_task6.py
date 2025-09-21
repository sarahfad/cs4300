import pytest
from pathlib import Path
import task6
from task6 import count_words

HERE = Path(__file__).parent
SRC_DIR = HERE.parent / "src"
ASSIGNMENT_FILE = SRC_DIR / "task6_read_me.txt"


def test_assignment_file_exists_and_counts():
    assert ASSIGNMENT_FILE.exists(), "Expected src/task6_read_me.txt to exist"
    n = count_words(str(ASSIGNMENT_FILE))
    assert isinstance(n, int)
    assert n > 0  #ensure non empty


#base cases
@pytest.mark.parametrize(
    "content, expected",
    [
        ("hello world", 2),
        ("one  two   three\nfour", 4),  
        ("a\nb\nc", 3),
        ("tabs\tand  spaces", 3),
        (" leading and trailing spaces ", 4),
    ]
)
def test_count_words_basic(tmp_path, content, expected):
    p = tmp_path / "sample.txt"
    p.write_text(content, encoding="utf-8")
    assert count_words(str(p)) == expected


# edge cases
@pytest.mark.parametrize(
    "content, expected",
    [
        ("", 0),
        ("   \n\t   ", 0),
        ("hi, there! it's ok.", 4),
        ("word---breaks ??? new  line", 4),
        ("café naïve façade", 3),
    ]
)
def test_count_words_edges(tmp_path, content, expected):
    p = tmp_path / "edge.txt"
    p.write_text(content, encoding="utf-8")
    assert count_words(str(p)) == expected


#errors 
def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        count_words("does_not_exist_12345.txt")
