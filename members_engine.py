# We used in-memory before mongo
MEMBERS_DB = {}

VALID_MEMBERSHIP_TYPES = [
    "Yoga",
    "Boxing",
    "Fitness",
    "Basketball",
    "Tenis",
    "Swimming"
]

def create_member(member_id, name, membership_type):
    # Tip kontrolü
    if membership_type not in VALID_MEMBERSHIP_TYPES:
        raise ValueError(f"Invalid membership type. Valid types are: {VALID_MEMBERSHIP_TYPES}")
    
    member = {
        "id": member_id,
        "name": name,
        "type": membership_type
    }
    
    # Kayıt
    MEMBERS_DB[member_id] = member
    return member

def get_member(member_id):
    return MEMBERS_DB.get(member_id)