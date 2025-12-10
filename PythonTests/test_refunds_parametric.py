import pytest
from pricing_engine import calculate_refund

# TEST Data: (Class, Entry, expected refund)
refund_scenarios = [
    # --- YOGA (Base Price: 200) ---
    # Rule:if entry < 2 then refund %100, if >=  %30 refund
    ("Yoga", 0, 200.0),   
    ("Yoga", 1, 200.0),  
    ("Yoga", 2, 60.0),    
    ("Yoga", 5, 60.0),    
    ("Yoga", 10, 60.0),   

    # --- BOXING (Base Price: 120) ---
    # Rule:if entry < 2 then refund %100, if >=  %50 refund
    ("Boxing", 0, 120.0),
    ("Boxing", 1, 120.0),
    ("Boxing", 2, 60.0),  # 120 * 0.50 = 60
    ("Boxing", 3, 60.0),
    ("Boxing", 8, 60.0),

    # --- FITNESS (Base Price: 80) ---
    # Rule:if entry < 2 then refund %100, if >=  %10 refund
    ("Fitness", 0, 80.0),
    ("Fitness", 1, 80.0),
    ("Fitness", 2, 8.0),  # 80 * 0.10 = 8
    ("Fitness", 4, 8.0),
    ("Fitness", 20, 8.0),

    # --- BASKETBALL (Base Price: 40) ---
    # Rule:if entry < 2 then refund %100, if >=  %40 refund
    ("Basketball", 0, 40.0),
    ("Basketball", 1, 40.0),
    ("Basketball", 2, 16.0), # 40 * 0.40 = 16
    ("Basketball", 6, 16.0),
    ("Basketball", 15, 16.0),

    # --- TENIS (Base Price: 90) ---
    # Rule:if entry < 2 then refund %100, if >=  %80 refund
    ("Tenis", 0, 90.0),
    ("Tenis", 1, 90.0),
    ("Tenis", 2, 72.0),   # 90 * 0.80 = 72
    ("Tenis", 3, 72.0),
    ("Tenis", 7, 72.0),

    # --- SWIMMING (Base Price: 30) ---
    # Rule:if entry < 2 then refund %100, if >=  %15 refund
    ("Swimming", 0, 30.0),
    ("Swimming", 1, 30.0),
    ("Swimming", 2, 4.5), 
    ("Swimming", 5, 4.5),
    ("Swimming", 12, 4.5),

    # Invalid entry
    ("Futbol", 1, 0),     
    ("Futbol", 0, 0),
]

@pytest.mark.parametrize("class_type, entrances, expected_refund", refund_scenarios)
def test_refund_calculations_parametric(class_type, entrances, expected_refund):
    calculated = calculate_refund(class_type, entrances)
    
    # Floating point comparison
    assert calculated == pytest.approx(expected_refund, rel=1e-2)