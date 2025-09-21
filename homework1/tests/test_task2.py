import pytest
import task2

@pytest.mark.parametrize(
    "func, expected, expected_type",
    [
        (task2.integer_num, 20, int),
        (task2.float_num, 2.12, float),
        (task2.strings, "Hello, World!", str),
        (task2.boolean, True, bool),
    ]
)
def test_data_types(func, expected, expected_type):
    result = func()
    assert result == expected
    assert isinstance(result, expected_type)
