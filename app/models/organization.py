from typing import Optional
from datetime import datetime
from bson import ObjectId

class Organization:
    def __init__(
        self,
        name: str,
        collection_name: str,
        admin_id: ObjectId,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = _id or ObjectId()
        self.name = name
        self.collection_name = collection_name
        self.admin_id = admin_id
        self.created_at = created_at or datetime.utcnow()

    def to_document(self):
        return {
            "_id": self.id,
            "name": self.name,
            "collection_name": self.collection_name,
            "admin_id": self.admin_id,
            "created_at": self.created_at,
        }

