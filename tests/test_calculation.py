import pytest

def add(x, y):
    return x+y

def subtract(x, y):
    return x-y

@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (1, 2, 3),
        (5, 9, 14),
        (8, 5, 13)
    ]
)


def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (1, 2, -1),
        (9, 5, 4),
        (8, 5, 3)
    ]
)
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected