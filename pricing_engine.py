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

def calculate_dynamic_price(class_type, hour):
    base_price = get_base_price(class_type)
    
    if base_price is None:
        return None
    
    # Business Rules
    if 6 <= hour < 12:
        return base_price * 0.80  # %20 discount
    elif 12 <= hour < 17:
        return base_price * 1.00  # Standard
    elif 17 <= hour < 24:
        return base_price * 1.10  # %10 surge
    else:
        return base_price
    