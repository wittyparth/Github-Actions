import math

import pytest

from src.main import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_add(calc):
    assert calc.add(2, 3) == 5


def test_subtract(calc):
    assert calc.subtract(5, 2) == 3


def test_multiply(calc):
    assert calc.multiply(3, 4) == 12


def test_divide(calc):
    assert calc.divide(7, 2) == 3.5


def test_divide_by_zero(calc):
    with pytest.raises(ValueError):
        calc.divide(1, 0)


def test_power(calc):
    assert calc.power(2, 3) == 8


def test_sqrt(calc):
    assert calc.sqrt(9) == 3


def test_sqrt_negative(calc):
    with pytest.raises(ValueError):
        calc.sqrt(-1)


def test_evaluate_simple(calc):
    # expression mixing operators
    result = calc.evaluate("2 + 3 * 4 - 1/2")
    assert math.isclose(result, 2 + 3 * 4 - 0.5, rel_tol=1e-9)


def test_evaluate_unsupported_node(calc):
    # function calls should not be allowed
    with pytest.raises(ValueError):
        calc.evaluate("__import__('os').system('echo no')")
