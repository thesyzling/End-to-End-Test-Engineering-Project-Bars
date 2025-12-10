import pytest
from members_engine import create_member, get_member

# NOT: 'clean_db' fixture'ına artık gerek yok çünkü Mock kullanıyoruz.
# Veritabanı bağlantısı taklit edildiği için gerçek veri kalıntısı oluşmaz.

def test_create_new_member(mocker):
    # 1. HAZIRLIK: members_engine içindeki veritabanı koleksiyonunu MOCK'luyoruz
    mock_collection = mocker.patch("members_engine.members_collection")
    
    # insert_one çağrıldığında hiçbir şey yapmasın (None dönsün)
    mock_collection.insert_one.return_value = None

    # 2. EYLEM
    result = create_member(1, "Ahmet Yilmaz", "Yoga")

    # 3. DOĞRULAMA
    # MongoDB kullanıldığı için artık 'id' yerine '_id' kontrolü yapıyoruz
    assert result["_id"] == 1
    assert result["name"] == "Ahmet Yilmaz"
    assert result["type"] == "Yoga"
    
    # '1 in MEMBERS_DB' yerine, insert metodunun çağrılıp çağrılmadığını kontrol ediyoruz
    mock_collection.insert_one.assert_called_once()

def test_create_member_invalid_type():
    # Bu işlem veritabanına gitmeden önce kod tarafında engellendiği için
    # mock kullanmasak da olur, ancak safe-guard olarak hata bekliyoruz.
    with pytest.raises(ValueError):
        create_member(2, "Mehmet", "GoldMember")

def test_create_member_old_type_fails():
    # Geçersiz tip (Student listeden çıkarılmıştı)
    with pytest.raises(ValueError):
        create_member(3, "Can", "Student")

def test_get_existing_member(mocker):
    # 1. HAZIRLIK
    mock_collection = mocker.patch("members_engine.members_collection")
    
    # Veritabanı sanki şu veriyi bulmuş gibi davransın:
    mock_collection.find_one.return_value = {
        "_id": 1, 
        "name": "Ayse", 
        "type": "Fitness"
    }

    # 2. EYLEM
    member = get_member(1)
    
    # 3. DOĞRULAMA
    assert member["name"] == "Ayse"
    assert member["type"] == "Fitness"

def test_get_non_existent_member(mocker):
    # 1. HAZIRLIK
    mock_collection = mocker.patch("members_engine.members_collection")
    
    # Veritabanı "bulamadım" (None) dönsün
    mock_collection.find_one.return_value = None

    # 2. EYLEM
    member = get_member(999)
    
    # 3. DOĞRULAMA
    assert member is None