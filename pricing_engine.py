def get_base_price(class_type):
    prices = {
        "Yoga": 200,
        "Boxing": 120,
        "Fitness": 80,
        "Basketball": 40,
        "Tenis": 90, 
        "Swimming": 30
    }
    return prices.get(class_type)

def calculate_dynamic_price(class_type, hour, membership_type="Standard"):
    base_price = get_base_price(class_type)
    
    if base_price is None:
        return None
    

    mem_multipliers = {
        "Student": 0.70,
        "Standard": 1.00,
        "Premium": 1.20
    }
    # for invalid types
    m_multiplier = mem_multipliers.get(membership_type, 1.00)
    # Business Rules
    if 6 <= hour <= 12:
        t_multiplier = 0.80  # %20 discount
    elif 12 <= hour < 17:
        t_multiplier = 1.00  # Standard
    elif 17 <= hour < 24:
        t_multiplier = 1.10 # %10 surge
    else:
        t_multiplier = 1.00

    final_price = base_price * m_multiplier * t_multiplier
    return round(final_price, 2)
    
def calculate_refund(class_type, entrances):
    base_price = get_base_price(class_type)
    
    # return 0 for invalid
    if base_price is None:
        return 0
        
    
    if entrances > 2:
        return base_price 
    
    # Refund amounts
    refund_rates = {
        "Yoga": 0.30,
        "Boxing": 0.50,
        "Fitness": 0.10,
        "Basketball": 0.40,
        "Tenis": 0.80,
        "Swimming": 0.15
    }
    
    # Take ratio
    return base_price * refund_rates.get(class_type, 0)
