import pytest
import priceing_engine import get_base_price

def test_get_base_price_yoga():
    # Yogo should be $200
    assert get_base_price("Yoga") == 200

def test_get_base_price_fitness():
    assert get_base_price("Fitness") == 80

def test_get_base_price_invalid():
    # None for invalid Class
    assert get_base_price("Tekwando") is None