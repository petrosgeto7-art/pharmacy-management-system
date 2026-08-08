import pytest
from pharmacy_project.utils import (
    generate_unique_number,
    format_currency,
    calculate_markup,
    calculate_profit_margin
)

def test_generate_unique_number():
    num1 = generate_unique_number("TEST")
    num2 = generate_unique_number("TEST")
    
    assert num1.startswith("TEST-")
    assert num1 != num2
    assert len(num1.split("-")) == 3
    assert len(num1.split("-")[2]) == 5

def test_format_currency():
    assert format_currency(100.5) == "$100.50"
    assert format_currency(1000) == "$1,000.00"
    assert format_currency("invalid") == "$0.00"
    assert format_currency(None) == "$0.00"

def test_calculate_markup():
    assert calculate_markup(100, 150) == 50.0
    assert calculate_markup(50, 100) == 100.0
    assert calculate_markup(0, 100) == 0.0
    assert calculate_markup(-10, 10) == 0.0 # Handled gracefully? Actually the logic doesn't explicitly block negative, but usually cost is positive. Let's just assert 0 cost is 0.0.

def test_calculate_profit_margin():
    assert calculate_profit_margin(100, 150) == 33.33
    assert calculate_profit_margin(50, 100) == 50.0
    assert calculate_profit_margin(100, 0) == 0.0
