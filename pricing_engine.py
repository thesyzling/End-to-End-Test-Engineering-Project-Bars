def get_base_price(class_type):
    prices = {
        "Yoga": 200,
        "Boxing": 120,
        "Fitness": 80,
        "Basketball": 40,
        "Tennis": 90, 
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
    
def calculate_refund(class_type, entrances):
    base_price = get_base_price(class_type)
    
    # return 0 for invalid
    if base_price is None:
        return 0
        
    
    if entrances < 2:
        return base_price 
    
    # Refund amounts
    refund_rates = {
        "Yoga": 0.30,
        "Boxing": 0.50,
        "Fitness": 0.10,
        "Basketball": 0.40,
        "Tennis": 0.80,
        "Swimming": 0.15
    }
    
    # Take ratio
    rate = refund_rates.get(class_type, 0)
    
    return base_price * rate
    
