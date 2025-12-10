import pytest
from reservation_engine import create_reservation

def test_capacity_check_with_mock(mocker):
    # 1. Mongo bağlantısını ve count_documents fonksiyonunu taklit et (Mock)
    mock_db = mocker.patch("reservation_engine.get_db")
    
    # Senaryo: Veritabanı "Dolu" desin (count_documents = 50 dönsün)
    # Zincirleme mock: db["reservations"].count_documents(...)
    mock_db.return_value.__getitem__.return_value.count_documents.return_value = 50
    
    # 2. Testi Çalıştır (Yoga kapasitesi 50, dolayısıyla hata vermeli)
    with pytest.raises(ValueError) as excinfo:
        create_reservation(1, "Yoga", "2025-05-01", 10)
    
    assert "Capacity full" in str(excinfo.value)

def test_create_reservation_success(mocker):
    # 1. Mongo'yu mockla
    mock_db = mocker.patch("reservation_engine.get_db")
    
    # Senaryo: Veritabanı "Boş" desin (count_documents = 0)
    mock_db.return_value.__getitem__.return_value.count_documents.return_value = 0
    
    # 2. Testi Çalıştır
    result = create_reservation(1, "Yoga", "2025-05-01", 10)
    
    # 3. insert_one çağrıldı mı kontrol et
    mock_db.return_value.__getitem__.return_value.insert_one.assert_called_once()
    assert result["status"] == "Active"