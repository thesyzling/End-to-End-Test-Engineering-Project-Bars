from database import members_collection
VALID_MEMBERSHIP_TYPES = ["Yoga", "Boxing", "Fitness", "Basketball", "Tenis", "Swimming"]

def create_member(member_id, name, membership_type):
    if membership_type not in VALID_MEMBERSHIP_TYPES:
        raise ValueError(f"Invalid membership type. Valid: {VALID_MEMBERSHIP_TYPES}")
    
    member_data = {
        "_id": member_id, # Mongo ID olarak kullanıyoruz
        "name": name,
        "type": membership_type
    }
    
    # Mongo'ya kaydet
    members_collection.insert_one(member_data)
    return member_data

def get_member(member_id):
    return members_collection.find_one({"_id": member_id})