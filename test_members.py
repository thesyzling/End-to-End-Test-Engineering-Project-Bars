# Dosya: test_members.py
import pytest
from members_engine import create_member, get_member, MEMBERS_DB

# Her testten önce veritabanını temizle
@pytest.fixture(autouse=True)
def clean_db():
    MEMBERS_DB.clear()

def test_create_new_member():
    # Valid Type: Yoga (Listenizden biri)
    result = create_member(1, "Ahmet Yilmaz", "Yoga")
    assert result["id"] == 1
    assert result["name"] == "Ahmet Yilmaz"
    assert result["type"] == "Yoga"
    # Veritabanına eklendi mi?
    assert 1 in MEMBERS_DB

def test_create_member_invalid_type():
    # Invalid type : GoldMember
    with pytest.raises(ValueError):
        create_member(2, "Mehmet", "GoldMember")

def test_create_member_old_type_fails():
    # old types should be failed
    with pytest.raises(ValueError):
        create_member(3, "Can", "Student")

def test_get_existing_member():
    # Valid Type: Fitness
    create_member(1, "Ayse", "Fitness")
    member = get_member(1)
    assert member["name"] == "Ayse"
    assert member["type"] == "Fitness"

def test_get_non_existent_member():
    member = get_member(999)
    assert member is None