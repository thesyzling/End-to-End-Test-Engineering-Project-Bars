import pytest
from unittest.mock import MagicMock
from reservation_engine import create_reservation, cancel_reservation

# ---------------------------------------------------------
# CREATE RESERVATION TESTLERİ
# ---------------------------------------------------------

def test_capacity_check_with_mock(mocker):
    mock_db = mocker.patch("reservation_engine.get_db")
    mock_db.return_value.__getitem__.return_value.count_documents.return_value = 50
    
    with pytest.raises(ValueError) as excinfo:
        create_reservation(1, "Yoga", "2025-05-01", 10)
    assert "Capacity full" in str(excinfo.value)

def test_create_reservation_success(mocker):
    mock_db = mocker.patch("reservation_engine.get_db")
    mock_db.return_value.__getitem__.return_value.count_documents.return_value = 0
    
    result = create_reservation(1, "Yoga", "2025-05-01", 10)
    
    mock_db.return_value.__getitem__.return_value.insert_one.assert_called_once()
    assert result["status"] == "Active"

# ---------------------------------------------------------
# CANCEL RESERVATION TESTLERİ
# ---------------------------------------------------------

def test_cancel_reservation_success(mocker):
    # 1. Mongo bağlantısını mockla
    mock_db = mocker.patch("reservation_engine.get_db")
    
    # Senaryo: find_one_and_update başarılı (bir sözlük döner)
    mock_db.return_value.__getitem__.return_value.find_one_and_update.return_value = {"_id": "existing_id", "status": "Cancelled"}

    # 2. Testi Çalıştır
    reservation_id = "existing_id"
    result = cancel_reservation(reservation_id)

    # 3. Kontrol
    mock_db.return_value.__getitem__.return_value.find_one_and_update.assert_called_once()
    assert result is not None

def test_cancel_reservation_not_found(mocker):
    # 1. Mongo bağlantısını mockla
    mock_db = mocker.patch("reservation_engine.get_db")
    
    # Senaryo: Kayıt bulunamadı (find_one_and_update None döner)
    mock_db.return_value.__getitem__.return_value.find_one_and_update.return_value = None

    reservation_id = "non_existent_id"

    # 2. Testi Çalıştır ve KeyError bekle
    # Kodun burada hata fırlattığı için pytest.raises kullanıyoruz
    with pytest.raises(KeyError) as excinfo:
        cancel_reservation(reservation_id)

    # 3. Hata mesajını kontrol et
    assert "Reservation not found" in str(excinfo.value)