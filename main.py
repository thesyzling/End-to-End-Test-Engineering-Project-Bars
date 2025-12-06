# main.py - GÜNCEL TAM SÜRÜM
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId

# Motorları import ediyoruz
from pricing_engine import calculate_dynamic_price, calculate_refund
from members_engine import create_member, get_member
# Database
from database import reservations_collection, members_collection

app = FastAPI(
    title="Fitness Center API (Cloud)",
    description="Ortak Veritabanı ile Çalışan Rezervasyon Sistemi"
)

# --- AYARLAR ---
CAPACITIES = {
    "Yoga": 50, "Boxing": 40, "Fitness": 250,
    "Basketball": 20, "Tennis": 15, "Tenis": 15, "Swimming": 30
}

# --- MODELLER ---
PyObjectId = Annotated[str, BeforeValidator(str)]

# 1. Müşteri Modeli (YENİ)
class MemberModel(BaseModel):
    id: int = Field(alias="_id") # Manuel ID vereceğiz (örn: 101)
    name: str
    membership_type: str # Yoga, Fitness vb.

# 2. Rezervasyon Modeli
class ReservationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    class_type: str
    member_name: str
    date: str
    hour: int
    price: Optional[float] = None
    status: str = "Active"

    class Config:
        populate_by_name = True

# --- ENDPOINTLER ---

@app.get("/")
def read_root():
    return {"message": "Sistem Bulutta Calisiyor! ☁️"}

# === A) MÜŞTERİ İŞLEMLERİ (Bunu Ekledik) ===

@app.post("/members", status_code=201)
def add_member(member: MemberModel):
    # members_engine.py içindeki fonksiyonu kullan
    try:
        # create_member fonksiyonu database'e yazar
        create_member(member.id, member.name, member.membership_type)
        return {"message": "Müşteri başarıyla eklendi", "member": member}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Eğer aynı ID ile eklemeye çalışırsanız hata verir (Duplicate Key)
        raise HTTPException(status_code=400, detail="Bu ID zaten kayıtlı veya bir hata oluştu.")

@app.get("/members/{member_id}")
def read_member_info(member_id: int):
    # Veritabanından çek
    member = get_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    return member

# === B) REZERVASYON İŞLEMLERİ ===

@app.post("/reservations", response_model=ReservationModel, status_code=201)
def create_reservation_endpoint(reservation: ReservationModel):
    # Kapasite Kontrolü
    max_capacity = CAPACITIES.get(reservation.class_type)
    if not max_capacity:
        raise HTTPException(status_code=400, detail="Gecersiz ders tipi.")

    current_count = reservations_collection.count_documents({
        "class_type": reservation.class_type,
        "date": reservation.date,
        "hour": reservation.hour,
        "status": "Active"
    })

    if current_count >= max_capacity:
        raise HTTPException(status_code=400, detail=f"Dolu! ({current_count}/{max_capacity})")

    # Fiyat Hesapla
    price = calculate_dynamic_price(reservation.class_type, reservation.hour)
    
    # Kaydet
    new_res = reservation.model_dump(by_alias=True, exclude=["id"])
    new_res["price"] = price
    new_res["status"] = "Active"
    
    result = reservations_collection.insert_one(new_res)
    created_res = reservations_collection.find_one({"_id": result.inserted_id})
    
    return created_res

@app.post("/reservations/{reservation_id}/cancel")
def cancel_reservation_endpoint(reservation_id: str, entrances_used: int = Body(..., embed=True)):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail="Gecersiz ID")

    res = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
    if not res:
        raise HTTPException(status_code=404, detail="Bulunamadi")

    refund = calculate_refund(res["class_type"], entrances_used)
    
    reservations_collection.update_one(
        {"_id": ObjectId(reservation_id)}, 
        {"$set": {"status": "Cancelled"}}
    )
    
    return {"status": "Cancelled", "refund": refund}