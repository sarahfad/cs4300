import pytest
from decimal import Decimal
from fractions import Fraction
import task4 
from task4 import calculate_discount

# duck typing
@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 0, 100),
        (100, 25, 75),
        (100, 100, 0),
        (59.99, 10, 59.99 - (59.99 * 10 / 100)),
        (Decimal("100"), Decimal("12.5"), Decimal("100") - (Decimal("100") * Decimal("12.5") / 100)),
        (Fraction(5, 2), Fraction(20, 1), Fraction(5, 2) - (Fraction(5, 2) * Fraction(20, 1) / 100)),
        (0, 50, 0),
    ]
)
def test_calculate_discount_happy(price, discount, expected):
    result = calculate_discount(price, discount)

    if isinstance(result, float):
        assert result == pytest.approx(expected, rel=1e-12, abs=1e-12)
    else:
        assert result == expected


#edge boundaries for discount: exactly 0% and 100%

@pytest.mark.parametrize("price", [0, 1, 100, 9999, Decimal("19.99"), Fraction(7, 3)])
def test_edges_zero_and_full_discount(price):
    # 0 leaves price unchanged
    res0 = calculate_discount(price, 0)
    if isinstance(res0, float):
        assert res0 == pytest.approx(price)
    else:
        assert res0 == price


    res100 = calculate_discount(price, 100)
    if isinstance(res100, float):
        assert res100 == pytest.approx(0.0)
    else:
        assert res100 == price - price  


# larger discount
@pytest.mark.parametrize("price", [10, 1000, Decimal("19.95"), Fraction(9, 2)])
def test_monotonicity(price):
    a = calculate_discount(price, 5)
    b = calculate_discount(price, 10)
    c = calculate_discount(price, 20)
    assert a >= b >= c
    assert b == calculate_discount(price, 10)

#bools are explicitly not allowed
@pytest.mark.parametrize(
    "price, discount",
    [
        (True, 10),
        (10, True),
        (False, 0),
        (0, False),
    ]
)
def test_reject_bools(price, discount):
    with pytest.raises(TypeError):
        calculate_discount(price, discount)

#non numeric values
class NoMath:
    """Object without numeric arithmetic support."""

@pytest.mark.parametrize(
    "price, discount",
    [
        ("100", 10),
        (100, "10"),
        (None, 10),
        (100, None),
        (NoMath(), 10),
        (100, NoMath()),
        (object(), 10),
        (100, object()),
    ]
)
def test_invalid_types(price, discount):
    with pytest.raises(TypeError):
        calculate_discount(price, discount)

#invalid values: negative price, discount outside 0 to 100
@pytest.mark.parametrize("price", [-1, -0.01, Decimal("-5"), Fraction(-1, 2)])
def test_negative_price(price):
    with pytest.raises(ValueError):
        calculate_discount(price, 10)

@pytest.mark.parametrize("discount", [-1, -0.001, 100.0001, Decimal("200"), Fraction(201, 2)])
def test_discount_out_of_range(discount):
    with pytest.raises(ValueError):
        calculate_discount(100, discount)

#large numbers 
@pytest.mark.parametrize("price, discount", [(10**12, 33), (Decimal("1e20"), Decimal("0.5"))])
def test_large_numbers(price, discount):
    result = calculate_discount(price, discount)
    if isinstance(result, float):
        assert result >= 0.0 - 1e-9
    else:
        assert result >= 0
    
