from typing import Optional
from datetime import datetime
from bson import ObjectId

class AdminUser:
    def __init__(
        self,
        email: str,
        password_hash: str,
        org_id: ObjectId,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = _id or ObjectId()
        self.email = email
        self.password_hash = password_hash
        self.org_id = org_id
        self.created_at = created_at or datetime.utcnow()

    def to_document(self):
        return {
            "_id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "org_id": self.org_id,
            "created_at": self.created_at,
        }

