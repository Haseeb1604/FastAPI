import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",
    [
        (1, 2, 3),
        (5, 9, 14),
        (8, 5, 13)
    ]
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected",
    [
        (1, 2, -1),
        (9, 5, 4),
        (8, 5, 3)
    ]
)
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected


def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_bank_deposit_amount(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize(
    "deposit, withdraw, expected",
    [
        (500, 200, 300),
        (1000, 500, 500),
        (400, 100, 300)
    ]
)
def test_bank_transactions(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_balance(zero_bank_account):
    with pytest.raises(Exception):
        zero_bank_account.withdraw(200)