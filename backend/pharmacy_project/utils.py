"""
Utility functions for generating unique identifiers and formatting values
throughout the pharmacy management system.
"""
import time
import random
import string
from datetime import datetime


def generate_unique_number(prefix: str = "PH") -> str:
    """Generate a unique reference number with a given prefix.
    
    Format: PREFIX-YYYYMMDD-XXXXX
    Example: SL-20260808-A3F7K
    """
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{date_part}-{random_part}"


def format_currency(amount, symbol="$") -> str:
    """Format a numeric amount as currency string."""
    try:
        return f"{symbol}{float(amount):,.2f}"
    except (ValueError, TypeError):
        return f"{symbol}0.00"


def calculate_markup(cost_price, selling_price) -> float:
    """Calculate the markup percentage between cost and selling price."""
    try:
        cost = float(cost_price)
        sell = float(selling_price)
        if cost <= 0:
            return 0.0
        return round(((sell - cost) / cost) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def calculate_profit_margin(cost_price, selling_price) -> float:
    """Calculate the profit margin percentage."""
    try:
        cost = float(cost_price)
        sell = float(selling_price)
        if sell <= 0:
            return 0.0
        return round(((sell - cost) / sell) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0
