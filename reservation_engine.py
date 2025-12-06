# DB before Mongo
RESERVATIONS_DB = {}
RESERVATION_ID_COUNTER = 1

# ReadME capacity rules
CAPACITY_LIMITS = {
    "Yoga": 50,
    "Boxing": 40,
    "Fitness": 250,
    "Basketball": 20,
    "Tenis": 15,
    "Swimming": 30
}

def check_capacity(class_type,date, hour):
    """
    True -> reservation done
    False -> out of capacity
    """
    limit = CAPACITY_LIMITS.get(class_type, 0)
    
    # Check the active reservations
    current_occupancy = sum(
        1 for r in RESERVATIONS_DB.values()
        if r["class_type"] == class_type 
        and r["date"] == date
        and r["hour"] == hour 
        and r["status"] == "Active"
    )
    
    return current_occupancy < limit

def create_reservation(member_id, class_type,date, hour):
    global RESERVATION_ID_COUNTER
    
    # 1- Capacity check
    if not check_capacity(class_type,date, hour):
        raise ValueError(f"Capacity full for {class_type} on {date}  at {hour}:00")

    # 2 - make reservation
    reservation = {
        "id": RESERVATION_ID_COUNTER,
        "member_id": member_id,
        "class_type": class_type,
        "date": date,
        "hour": hour,
        "status": "Active"
    }
    
    RESERVATIONS_DB[RESERVATION_ID_COUNTER] = reservation
    RESERVATION_ID_COUNTER += 1
    
    return reservation

def cancel_reservation(reservation_id):
    if reservation_id not in RESERVATIONS_DB:
        raise KeyError("Reservation not found")
    
    # status update
    RESERVATIONS_DB[reservation_id]["status"] = "Cancelled"
    return RESERVATIONS_DB[reservation_id]