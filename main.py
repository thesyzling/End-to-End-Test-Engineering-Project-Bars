from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles  
from fastapi.responses import FileResponse   

# Engine dosyalarınızdan fonksiyonları çekiyoruz
from pricing_engine import calculate_dynamic_price, calculate_refund, get_base_price
from members_engine import create_member, get_member
from reservation_engine import create_reservation, cancel_reservation

app = FastAPI(
    title="Fitness Center API",
    description="End-to-End Test Engineering Project API with MongoDB",
    version="2.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- PYDANTIC MODELLERİ (Veri Doğrulama) ---

class MemberRequest(BaseModel):
    name: str
    membership_type: str  # Valid: Yoga, Boxing, Fitness, Basketball, Tenis, Swimming

class ReservationRequest(BaseModel):
    member_id: int
    class_type: str
    date: str  # Format: "YYYY-MM-DD"
    hour: int  # 0-23

class PriceResponse(BaseModel):
    class_type: str
    hour: int
    estimated_price: float
    currency: str = "USD"

# --- 1. GENERAL ENDPOINTS
@app.get("/ui", include_in_schema=False)
def read_ui():
    return FileResponse('static/index.html')

@app.get("/", tags=["General"])
def read_root():
    return {"message": "CEN315 Test Engineering API is Online 🟢"}

@app.get("/price/{class_type}/{hour}", tags=["General"], response_model=PriceResponse)
def check_price(class_type: str, hour: int):
    """
    check before rezervation
    """
    price = calculate_dynamic_price(class_type, hour)
    if price is None:
        raise HTTPException(status_code=404, detail="Class type not found")
    
    return {
        "class_type": class_type,
        "hour": hour,
        "estimated_price": round(price, 2)
    }

# --- 2. Member Management

@app.post("/members", status_code=status.HTTP_201_CREATED, tags=["Members"])
def register_new_member(member: MemberRequest):
    """
    Save new member. (MongoDB)
    """
    import random
    new_id = random.randint(1000, 9999) # Sımilation ID
    
    try:
        result = create_member(new_id, member.name, member.membership_type)
        # MongoDB _id nesnesini string'e veya int'e çevirip dönmek daha güvenlidir
        result["_id"] = str(result["_id"]) 
        return {
            "message": "User registered successfully",
            "member_id": new_id,
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/members/{member_id}", tags=["Members"])
def get_member_profile(member_id: int):
    """
    Bring the new member
    """
    member = get_member(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Mongo ObjectId serileştirme hatası olmaması için
    if "_id" in member:
        member["_id"] = str(member["_id"])
        
    return member

# --- 3. REZERVASYON YÖNETİMİ (Tags: Reservations) ---

@app.post("/reservations", status_code=status.HTTP_201_CREATED, tags=["Reservations"])
def make_reservation(request: ReservationRequest):
    """
    Make new rezervations
    """
    # 1. Üye kontrolü
    member = get_member(request.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found. Please register first.")
    
    mem_type = member.get("type", "Standard")

    # 2. Ders tipi kontrolü
    if get_base_price(request.class_type) is None:
        raise HTTPException(status_code=400, detail="Invalid class type.")

    try:
        # 3. Rezervasyon ve Kapasite
        reservation = create_reservation(
            member_id=request.member_id,
            class_type=request.class_type,
            date=request.date,
            hour=request.hour
        )
        
        # 4. Fiyat Bilgisi Ekleme
        price = calculate_dynamic_price(request.class_type, request.hour, membership_type=mem_type)
        reservation["price"] = round(price, 2)
        
        # Mongo ID temizliği
        if "_id" in reservation:
            reservation["_id"] = str(reservation["_id"])
            
        return reservation

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reservations/{reservation_id}", tags=["Reservations"])
def delete_reservation(reservation_id: int, entrances_used: int = 0):
    """
    Cancel rezervations
    """
    try:
        # İptal işlemi
        reservation = cancel_reservation(reservation_id)
        
        # İade hesabı
        refund = calculate_refund(reservation["class_type"], entrances_used)
        
        return {
            "status": "cancelled",
            "reservation_id": reservation_id,
            "refund_amount": round(refund, 2),
            "info": "Refund calculated based on usage."
        }
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Reservation ID not found.")