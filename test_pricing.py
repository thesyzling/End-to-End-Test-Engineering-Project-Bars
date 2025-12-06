import pytest
from pricing_engine import get_base_price
from pricing_engine import calculate_dynamic_price

def test_get_base_price_yoga():
    # Yogo should be $200
    assert get_base_price("Yoga") == 200

def test_get_base_price_fitness():
    assert get_base_price("Fitness") == 80

def test_get_base_price_invalid():
    # None for invalid Class
    assert get_base_price("Tekwando") is None

# new push after adding actions

def test_price_morning_discount():
    # 06.00 - 12.00 % 20 discount
    # ex: Yoga should be 160 dolars
    assert calculate_dynamic_price("Yoga", 9) == 160.0

def test_price_standard_hours():
    # 12.00 - 17.00 normal price
    # ex: Boxing should be 120
    assert calculate_dynamic_price("Boxing", 14) == 120.0

def test_price_evening_surge():
    #17.00 - 24.00 %10 surge
    #ex: Fitness
    assert calculate_dynamic_price("Fitness", 18) == 88.0
