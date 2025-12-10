import pytest
from pricing_engine import calculate_dynamic_price

# Format: (Class, hour, mem_type, expected rate)
test_data = [
    # --- YOGA (Base: 200) ---
    # Student (%30 discount -> Base: 140)
    ("Yoga", 8, "Student", 112.0),   # Sabah: 140 * 0.8 = 112
    ("Yoga", 14, "Student", 140.0),  # Öğle: 140 * 1.0 = 140
    ("Yoga", 19, "Student", 154.0),  # Akşam: 140 * 1.1 = 154
    # Standard (Base: 200)
    ("Yoga", 8, "Standard", 160.0),  # Sabah: 200 * 0.8 = 160
    ("Yoga", 14, "Standard", 200.0), # Öğle: 200 * 1.0 = 200
    ("Yoga", 19, "Standard", 220.0), # Akşam: 200 * 1.1 = 220
    # Premium (%20 Zam -> Base: 240)
    ("Yoga", 8, "Premium", 192.0),   # Sabah: 240 * 0.8 = 192
    ("Yoga", 14, "Premium", 240.0),  # Öğle: 240 * 1.0 = 240
    ("Yoga", 19, "Premium", 264.0),  # Akşam: 240 * 1.1 = 264

    # --- BOXING (Base: 120) ---
    # Student (Base: 84)
    ("Boxing", 8, "Student", 67.2),
    ("Boxing", 14, "Student", 84.0),
    ("Boxing", 19, "Student", 92.4),
    # Standard (Base: 120)
    ("Boxing", 8, "Standard", 96.0),
    ("Boxing", 14, "Standard", 120.0),
    ("Boxing", 19, "Standard", 132.0),
    # Premium (Base: 144)
    ("Boxing", 8, "Premium", 115.2),
    ("Boxing", 14, "Premium", 144.0),
    ("Boxing", 19, "Premium", 158.4),

    # --- FITNESS (Base: 80) ---
    # Student (Base: 56)
    ("Fitness", 9, "Student", 44.8),
    ("Fitness", 15, "Student", 56.0),
    ("Fitness", 20, "Student", 61.6),
    # Standard (Base: 80)
    ("Fitness", 9, "Standard", 64.0),
    ("Fitness", 15, "Standard", 80.0),
    ("Fitness", 20, "Standard", 88.0),
    # Premium (Base: 96)
    ("Fitness", 9, "Premium", 76.8),
    ("Fitness", 15, "Premium", 96.0),
    ("Fitness", 20, "Premium", 105.6),

    # --- BASKETBALL (Base: 40) ---
    # Student (Base: 28)
    ("Basketball", 10, "Student", 22.4),
    ("Basketball", 13, "Student", 28.0),
    ("Basketball", 21, "Student", 30.8),
    # Standard (Base: 40)
    ("Basketball", 10, "Standard", 32.0),
    ("Basketball", 13, "Standard", 40.0),
    ("Basketball", 21, "Standard", 44.0),
    # Premium (Base: 48)
    ("Basketball", 10, "Premium", 38.4),
    ("Basketball", 13, "Premium", 48.0),
    ("Basketball", 21, "Premium", 52.8),
    
    # --- TENIS (Base: 90) ---
    # Student (Base: 63)
    ("Tenis", 7, "Student", 50.4),
    ("Tenis", 12, "Student", 63.0),
    ("Tenis", 18, "Student", 69.3),
    # Standard (Base: 90)
    ("Tenis", 7, "Standard", 72.0),
    ("Tenis", 12, "Standard", 90.0),
    ("Tenis", 18, "Standard", 99.0),
    # Premium (Base: 108)
    ("Tenis", 7, "Premium", 86.4),
    ("Tenis", 12, "Premium", 108.0),
    ("Tenis", 18, "Premium", 118.8),

    # --- SWIMMING (Base: 30) ---
    # Student (Base: 21)
    ("Swimming", 6, "Student", 16.8),
    ("Swimming", 16, "Student", 21.0),
    ("Swimming", 23, "Student", 23.1),
    # Standard (Base: 30)
    ("Swimming", 6, "Standard", 24.0),
    ("Swimming", 16, "Standard", 30.0),
    ("Swimming", 23, "Standard", 33.0),
    # Premium (Base: 36)
    ("Swimming", 6, "Premium", 28.8),
    ("Swimming", 16, "Premium", 36.0),
    ("Swimming", 23, "Premium", 39.6),
]

@pytest.mark.parametrize("class_type, hour, membership_type, expected_price", test_data)
def test_dynamic_pricing_combinations(class_type, hour, membership_type, expected_price):
    """
    Bu tek fonksiyon, yukarıdaki listedeki her satır için ayrı ayrı çalışır.
    Toplamda 54 adet Unit Test oluşturur.
    """
    calculated = calculate_dynamic_price(class_type, hour, membership_type)
    # Floating point hatası olmaması için yaklaşık değer kontrolü (pytest.approx)
    assert calculated == pytest.approx(expected_price, rel=1e-2)