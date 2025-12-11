from fastapi import HTTPException, status
from bson import ObjectId

from ..db import admins_collection
from ..utils.security import verify_password, create_access_token

class AuthService:
    def __init__(self):
        self.admins = admins_collection

    def admin_login(self, email: str, password: str) -> str:
        admin = self.admins.find_one({"email": email})
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        if not verify_password(password, admin["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        token = create_access_token(
            data={
                "sub": str(admin["_id"]),
                "admin_id": str(admin["_id"]),
                "org_id": str(admin["org_id"]),
                "email": admin["email"],
            }
        )

        return token

    def parse_admin_from_token_payload(self, payload: dict) -> tuple[ObjectId, ObjectId]:
        admin_id = payload.get("admin_id")
        org_id = payload.get("org_id")
        if not admin_id or not org_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )
        return ObjectId(admin_id), ObjectId(org_id)

