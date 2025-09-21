import pytest
from task3 import define_number, is_prime, first_10_primes, print_first_10_primes, sum_1_to_100


# define_number tests

@pytest.mark.parametrize(
    "x, expected",
    [(1, "positive"), (999, "positive"), (-1, "negative"), (-42, "negative"), (0, "zero")]
)
def test_define_number_values(x, expected):
    assert define_number(x) == expected

@pytest.mark.parametrize("bad", [True, False, 3.14, "0", None, complex(2, 1)])
def test_define_number_type_errors(bad):
    with pytest.raises(TypeError):
        define_number(bad)


# is_prime tests

@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
def test_is_prime_true(n):
    assert is_prime(n) is True

@pytest.mark.parametrize("n", [0, 1, 4, 6, 8, 9, 12, 15, 21, 25, 100])
def test_is_prime_false(n):
    assert is_prime(n) is False

@pytest.mark.parametrize("bad", [True, 2.0, "3", None])
def test_is_prime_type_error(bad):
    with pytest.raises(TypeError):
        is_prime(bad)

# first_10_primes + print tests

def test_first_10_primes_exact_list():
    assert first_10_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_print_first_10_primes_output(capsys):
    print_first_10_primes()
    captured = capsys.readouterr().out.strip().splitlines()
    assert [int(x) for x in captured] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_first_10_primes_increasing_and_prime():
    arr = first_10_primes()
    assert arr == sorted(arr)
    assert all(is_prime(x) for x in arr)


# sum_1_to_100 tests


def test_sum_1_to_100_value():
    assert sum_1_to_100() == 5050

