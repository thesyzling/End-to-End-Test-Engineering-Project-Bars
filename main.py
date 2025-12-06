from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# TDD motor import (pricing_engine.py, members_engine.py, reservation_engine.py)
from pricing_engine import get_base_price, calculate_dynamic_price, calculate_refund
from members_engine import create_member, get_member
from reservation_engine import create_reservation, cancel_reservation

app = FastAPI(
    title="Fitness Center API",
    description="End-to-End Test Engineering Project API",
    version="1.0.0"
)

# --- PYDANTIC MODELS (Data Validation) ---

class MemberRequest(BaseModel):
    name: str
    membership_type: str  # Valid: Yoga, Boxing, Fitness, etc.

class ReservationRequest(BaseModel):
    member_id: int
    class_type: str
    date: str  # Format: "YYYY-MM-DD"
    hour: int  # 0-23


@app.get("/")
def read_root():
    return {"message": "CEN315 Test Engineering Project API is Running 🚀"}

# --- 1. MEMBERSHIP MANAGEMENT

@app.post("/members", status_code=status.HTTP_201_CREATED)
def add_new_member(member: MemberRequest):
    """
    Saves new members
    Engine: members_engine.py
    """
    # Simple ID production
    # Until DB-Mongo
    import random
    new_id = random.randint(1000, 9999) 
    
    try:
        result = create_member(new_id, member.name, member.membership_type)
        return result
    except ValueError as e:
        # 400 for invalid member
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/members/{member_id}")
def read_member(member_id: int):
    """
    Brings the member info
    Engine: members_engine.py
    """
    member = get_member(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# --- 2. Price check

@app.get("/price/{class_type}/{hour}")
def check_price(class_type: str, hour: int):
    """
    Shows the price before reservation
    Engine: pricing_engine.py
    """
    price = calculate_dynamic_price(class_type, hour)
    if price is None:
        raise HTTPException(status_code=404, detail="Class type not found")
    
    return {
        "class_type": class_type,
        "hour": hour,
        "estimated_price": round(price, 2),
        "currency": "USD"
    }

# --- 3. Reservation Management

@app.post("/reservations", status_code=status.HTTP_201_CREATED)
def make_reservation(request: ReservationRequest):
    """
    Make the reservation
    Capacity and Date
    Engines: reservation_engine.py, members_engine.py, pricing_engine.py
    """
    # Step 1: Check member
    member = get_member(request.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found. Please register first.")

    # Step 2: check to if its invalid
    if get_base_price(request.class_type) is None:
        raise HTTPException(status_code=400, detail="Invalid class type.")

    try:
        # Step 3: Make reservations
        reservation = create_reservation(
            member_id=request.member_id,
            class_type=request.class_type,
            date=request.date,
            hour=request.hour
        )
        
        # Step 4: Calculate the price and add to sum
        price = calculate_dynamic_price(request.class_type, request.hour)
        reservation["price"] = round(price, 2)
        
        return reservation

    except ValueError as e:
        # Capacity and date error
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, entrances_used: int = 0):
    """
    Cancel reservation and get a refund
    Engine: reservation_engine.py, pricing_engine.py
    """
    try:
        # Step 1: Cancel process
        # Error if no reservations
        reservation = cancel_reservation(reservation_id)
        
        # Adım 2: calculate to refund amunt
        refund = calculate_refund(reservation["class_type"], entrances_used)
        
        return {
            "status": "cancelled",
            "reservation_id": reservation_id,
            "original_date": reservation["date"],
            "refund_amount": round(refund, 2),
            "message": "Reservation cancelled successfully."
        }
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Reservation ID not found.")
