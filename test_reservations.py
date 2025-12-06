import pytest
from reservation_engine import create_reservation, cancel_reservation, RESERVATIONS_DB

# clead the DB
@pytest.fixture(autouse=True)
def clean_db():
    RESERVATIONS_DB.clear()

def test_create_valid_reservation():
    # Reservation to empty yoga class
    # Üye ID: 1, Ders: Yoga, Saat: 10
    result = create_reservation(member_id=1, class_type="Yoga", hour=10)
    
    assert result["status"] == "Active"
    assert result["class_type"] == "Yoga"
    assert 1 in RESERVATIONS_DB

def test_capacity_limit_exceeded():
    # Capacity of tennis is 15, test for more
    for i in range(15):
        create_reservation(member_id=i+100, class_type="Tenis", hour=14)
        
    # error in 16
    with pytest.raises(ValueError) as excinfo:
        create_reservation(member_id=999, class_type="Tenis", hour=14)
    
    assert "Capacity full" in str(excinfo.value)

def test_cancel_reservation():
    # make reservation
    res = create_reservation(member_id=1, class_type="Boxing", hour=18)
    res_id = res["id"]
    
    # then cancel it
    canceled_res = cancel_reservation(res_id)
    
    assert canceled_res["status"] == "Cancelled"
    # Check DB
    assert RESERVATIONS_DB[res_id]["status"] == "Cancelled"

def test_cancel_non_existent_reservation():
    with pytest.raises(KeyError):
        cancel_reservation(99999)