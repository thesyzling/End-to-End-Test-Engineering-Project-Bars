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
    