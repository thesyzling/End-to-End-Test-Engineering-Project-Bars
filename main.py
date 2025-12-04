# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pricing_engine import get_base_price, calculate_dynamic_price, calculate_refund
# NOT: main.py'ın pricing_engine.py'ı import edebilmesi için aynı klasörde olmaları gerekir.

app = FastAPI(
    title="Fitness Center API",
    description="Dynamic Pricing and Reservation Service for CEN315 Project"
)

# Rezervasyon Modelini Tanımlama (Pydantic)
# Gerçek bir veritabanı yerine, rezervasyonları bellekte tutacağız (basitlik için)
RESERVATIONS = {}
reservation_id_counter = 0

class ReservationRequest(BaseModel):
    class_type: str
    member_name: str
    hour: int
    # Eğer isterseniz, burada Capacity kontrolü için gereken diğer bilgileri de ekleyebilirsiniz.
    
class Reservation(ReservationRequest):
    id: int
    price: float
    status: str = "Active"

# ----------------- ENDPOINTLER -----------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Test Engineering Project API"}

# 1. Fiyat Hesaplama Endpointi
# Kullanıcıya rezervasyon yapmadan önce dinamik fiyatı gösterir.
@app.get("/price/{class_type}/{hour}")
def get_current_price(class_type: str, hour: int):
    price = calculate_dynamic_price(class_type, hour)
    if price is None:
        raise HTTPException(status_code=404, detail=f"Class type '{class_type}' not found.")
    return {"class_type": class_type, "hour": hour, "price": round(price, 2)}

# 2. Rezervasyon Endpointi
# Burada kapasite kontrolü gibi ek mantıklar eklemelisiniz.
@app.post("/reservations")
def create_reservation(request: ReservationRequest):
    global reservation_id_counter
    reservation_id_counter += 1
    
    # Fiyatı hesapla
    price = calculate_dynamic_price(request.class_type, request.hour)
    if price is None:
        raise HTTPException(status_code=400, detail="Invalid class type.")

    # BASİT KAPASİTE KONTROLÜ (Geliştirmeniz gerekiyor)
    # Gerçek projede, saat ve ders tipine göre o anki doluluğu kontrol etmeniz gerekir.

    reservation = Reservation(
        id=reservation_id_counter,
        price=round(price, 2),
        **request.model_dump() # Pydantic v2 için **request.model_dump() kullanıldı
    )
    RESERVATIONS[reservation.id] = reservation
    
    return reservation

# 3. İptal Endpointi
@app.post("/reservations/{reservation_id}/cancel")
def cancel_reservation(reservation_id: int, entrances_used: int):
    if reservation_id not in RESERVATIONS:
        raise HTTPException(status_code=404, detail="Reservation not found.")
        
    reservation = RESERVATIONS[reservation_id]
    
    # İadeyi hesapla
    refund_amount = calculate_refund(reservation.class_type, entrances_used)
    
    # Rezervasyon durumunu güncelle
    reservation.status = "Cancelled"
    
    return {"status": "success", "reservation_id": reservation_id, "refund_amount": round(refund_amount, 2)}