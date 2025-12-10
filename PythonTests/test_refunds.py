import pytest
from pricing_engine import calculate_refund 

def test_refund_before_two_entrances():
    # Yoga (200) -> 200 refund
    assert calculate_refund("Yoga", entrances=1) == 200

def test_refund_after_limit_yoga():
    # Yoga refund %30
    # Yoga (200) -> 60 refund
    assert calculate_refund("Yoga", entrances=3) == 60

def test_refund_after_limit_boxing():
    # Boxing %50
    # Boxing (120) -> 60 refund
    assert calculate_refund("Boxing", entrances=5) == 60

def test_refund_invalid_class():
    # zero for none class
    assert calculate_refund("Karate", entrances=1) == 0